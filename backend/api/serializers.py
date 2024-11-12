from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UserInterest, ArticleData

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class UserInterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInterest
        fields = ['id', 'user', 'company_name']

class ArticleDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleData
        fields = ['id', 'interest', 'link', 'date', 'text']

    

