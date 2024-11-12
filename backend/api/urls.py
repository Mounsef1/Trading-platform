from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register the viewsets
router = DefaultRouter()
router.register(r'user-interests', views.UserInterestViewSet, basename='user-interest')
router.register(r'articles', views.ArticleDataViewSet, basename='article-data')

urlpatterns = [
    path("user/details/", views.UserDetailView.as_view(), name="user-details"),
    path('', include(router.urls)),  # Include the router-generated routes
]
