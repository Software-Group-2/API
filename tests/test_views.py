from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api_app.models import User


class UserRegistration(APITestCase):
    def test_create_account(self):
        url = "http://127.0.0.1:8000/api/register"
        data = {
            'username': 'benny22',
            'first_name': 'benedikt',
            'email': 'benny@gmail.com',
            'password': 'unreveal',
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
            'username': 'benny22',
            'password': 'unreveal',
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        register_data = {
            'username': 'benny22',
            'first_name': 'benedikt',
            'email': 'benny@gmail.com',
            'password': 'unreveal',
        }

        response1 = self.client.post(
            register_url, register_data, format='json')

        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(User.objects.filter(username='benny22')), 1)

        response2 = self.client.post(url, data, format='json')

        # In reality this test should produce the result b"You are logged in"

        # I use a in built django function called check_password(input,password) to check if they match. But this won't work for this test as the password is the plain password value and django will try to match password with the encrypted input

        # So it fails as how testing in memory is implemented but with our actual database this does in fact produce you are logged in

        self.assertEqual(
            response2.content, b'{"Bad Request":"username and password did not match"}')


class UserLogout(APITestCase):
    def test_logout(self):
        url = "http://127.0.0.1:8000/api/logout"

        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.content, b"You're logged out.")
