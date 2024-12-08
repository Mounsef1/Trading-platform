from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'user-interests', views.UserInterestViewSet, basename='user-interest')
router.register(r'articles', views.ArticleDataViewSet, basename='article-data')

urlpatterns = [
    path("user/details/", views.UserDetailView.as_view(), name="user-details"),
    path('', include(router.urls)),
    path('generate-wordcloud/<int:interest_id>/', views.generate_wordcloud_and_sentiment, name='generate_wordcloud_and_sentiment'),
    path('sources/', views.get_sources, name='get_sources'),
    # Add this line for the time-series sentiment data
    path('sentiment-timeseries/<int:interest_id>/', views.sentiment_time_series, name='sentiment-time-series'),
]
