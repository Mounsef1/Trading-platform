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
from .scraper import scrap_articles_bbc  # Import your scraping function
from django.utils.timezone import now
import json
import logging

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

        # Step 1: Delete existing articles for the user's interest
        ArticleData.objects.filter(interest=user_interest).delete()

        # Step 2: Run the scraping function for the specified interest
        articles_json = scrap_articles_bbc([company_name])
        articles = json.loads(articles_json)

        # Step 3: Save new articles to the database
        for article in articles:
            ArticleData.objects.create(
                interest=user_interest,
                link=article['Link'],
                date=now().date(),
                text=article['Text']
            )

        return Response({"message": "Articles scraped and saved successfully."}, status=status.HTTP_201_CREATED)



class ArticleDataViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ArticleData.objects.all()
    serializer_class = ArticleDataSerializer

