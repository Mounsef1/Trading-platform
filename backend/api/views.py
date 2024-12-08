from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import UserInterest, ArticleData
from .serializers import UserInterestSerializer, ArticleDataSerializer
from .scraper import scrape_articles
from django.utils.timezone import now
import json
import logging
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from rest_framework.decorators import api_view
from django.http import JsonResponse
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
import requests
import json
import pandas as pd
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)




class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]



class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'id': user.id,
            'username': user.username
        })




from django.utils.timezone import now

class UserInterestViewSet(viewsets.ModelViewSet):
    queryset = UserInterest.objects.all()
    serializer_class = UserInterestSerializer
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can create interests

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['user'] = request.user.id  # Automatically assign the authenticated user

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=['post'])
    def run_scraper(self, request, pk=None):
        user_interest = self.get_object()
        company_name = user_interest.company_name

        # Delete existing articles for the user's interest
        ArticleData.objects.filter(interest=user_interest).delete()

        # Fetch articles
        articles = scrape_articles(company_name, days=7)

        # Save articles to the database
        for article in articles:
            ArticleData.objects.create(
                interest=user_interest,
                link=article['link'],
                date=datetime.fromisoformat(article['date']).date(),
                text=article['text'],
                source=article['source']  # Save the source field
            )

        return Response({"message": "Articles scraped and saved successfully."}, status=status.HTTP_201_CREATED)

            

class ArticleDataViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ArticleData.objects.all()
    serializer_class = ArticleDataSerializer

nltk.download('vader_lexicon')  # Download sentiment analysis data

@api_view(['GET'])
def generate_wordcloud_and_sentiment(request, interest_id):
    try:
        # Retrieve source parameter from query string
        source = request.query_params.get('source', None)

        # Retrieve articles for the selected interest, optionally filtering by source
        if source:
            articles = ArticleData.objects.filter(interest_id=interest_id, source=source)
        else:
            articles = ArticleData.objects.filter(interest_id=interest_id)

        if not articles.exists():
            return JsonResponse({"error": "No articles found for this interest."}, status=404)

        # Combine all article texts
        all_text = " ".join(article.text for article in articles)

        # Generate word cloud
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_text)
        buffer = BytesIO()
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        buffer.close()

        # Perform sentiment analysis
        sia = SentimentIntensityAnalyzer()
        sentiment = sia.polarity_scores(all_text)

        return JsonResponse({
            "wordcloud": image_base64,
            "sentiment": sentiment  # e.g., {'neg': 0.1, 'neu': 0.8, 'pos': 0.1, 'compound': 0.0}
        })
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@api_view(['GET'])
def get_sources(request):
    sources = ArticleData.objects.values_list('source', flat=True).distinct()
    return JsonResponse(list(sources), safe=False)


@api_view(['GET'])
def sentiment_time_series(request, interest_id):
    try:
        source = request.GET.get('source', None)

        # Filter articles by interest and source
        articles = ArticleData.objects.filter(interest_id=interest_id)
        if source:
            articles = articles.filter(source=source)

        if not articles.exists():
            return JsonResponse({"error": "No articles found for this interest."}, status=404)

        # Perform sentiment analysis grouped by date
        sia = SentimentIntensityAnalyzer()
        sentiment_by_date = {}
        for article in articles:
            sentiment = sia.polarity_scores(article.text)
            date = article.date
            if date not in sentiment_by_date:
                sentiment_by_date[date] = {"pos": [], "neu": [], "neg": []}
            sentiment_by_date[date]["pos"].append(sentiment["pos"])
            sentiment_by_date[date]["neu"].append(sentiment["neu"])
            sentiment_by_date[date]["neg"].append(sentiment["neg"])

        # Aggregate sentiment scores for each date
        result = [
            {
                "date": date,
                "pos": sum(values["pos"]) / len(values["pos"]),
                "neu": sum(values["neu"]) / len(values["neu"]),
                "neg": sum(values["neg"]) / len(values["neg"]),
            }
            for date, values in sentiment_by_date.items()
        ]

        # Sort results by date
        result.sort(key=lambda x: x["date"])

        return JsonResponse(result, safe=False)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

