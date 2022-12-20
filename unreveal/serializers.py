from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Place, Comment, ErrorResponse, SuccessResponse, Rating


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']


class LogoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = [
            'id',
            'email',
            'latitude',
            'longitude',
            'name',
            'description',
            'label',
        ]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'place_id', 'email', 'comment']


class ErrorResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ErrorResponse
        fields = ['error', 'description']


class SuccessResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuccessResponse
        fields = ['message', 'description']


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'place_id', 'email', 'rating']
