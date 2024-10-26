from django.urls import path
from . import views

urlpatterns = [
    path("user/details/", views.UserDetailView.as_view(), name="user-details"), 
]