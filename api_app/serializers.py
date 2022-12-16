from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Place, Comment, ErrorResponse, SuccessResponse


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = [
            'id',
            'username',
            'latitude',
            'longitude',
            'name',
            'description',
            'label',
        ]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'place_id', 'username', 'comment']


class ErrorResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ErrorResponse
        fields = ['error', 'description']


class SuccessResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuccessResponse
        fields = ['message', 'description']
