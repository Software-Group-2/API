from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api_app.models import User


class UserRegistration(APITestCase):
    def test_create_account(self):
        url = "http://127.0.0.1:8000/api/register"
        data = {
            "username": "benny22",
            "email": "benny@gmail.com",
            "password": "unreveal"
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(User.objects.filter(username='benny22')), 1)

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class UserLogin(APITestCase):
    def test_login(self):
        print(User.objects.all())
        url = "http://127.0.0.1:8000/api/login"
        register_url = "http://127.0.0.1:8000/api/register"

        data = {
            "username": "benny22",
            "password": "unreveal"
            }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        register_data = {
            "username": "benny22",
            "email": "benny@gmail.com",
            "password": "unreveal"
            }

        response1 = self.client.post(
            register_url, register_data, format="json")

        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(User.objects.filter(username="benny22")), 1)

        response2 = self.client.post(url, data, format="json")

        self.assertEqual(
            response2.content,  b"You are logged in")


class UserLogout(APITestCase):
    def test_logout(self):
        url = "http://127.0.0.1:8000/api/logout"

        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.content, b"You're logged out.")
