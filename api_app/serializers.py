from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Place

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class LoginUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']


class AddPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ['latitude', 'longitude','place', 'description', 'label']
