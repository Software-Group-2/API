from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api_app.models import User,Place



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


class AddPlaceTest(APITestCase):
    def test_create_account(self):
        url = "http://127.0.0.1:8000/api/addPlace"
        data = {
            "username": "benny",
            "latitude": "1234657865",
            "longitude": "456786754",
            "place": "caffee",
            "description": "best caffee in berlin",
            "label": "caffe;relax;fun",
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class AddCommentTest(APITestCase):
    def test_create_account(self):
        url = "http://127.0.0.1:8000/api/addComment"
        data = {
            "post_id": "1",
            "sender_id": "5b",
            "comment": "Hi im here for testing",

        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class GetCommentTest(APITestCase):
    def test_create_account(self):
        url = "http://127.0.0.1:8000/api/addComment"
        data = {
            "post_id": "1",
            "sender_id": "5b",
            "comment": "Hi im here for testing",

        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url = "http://127.0.0.1:8000/api/get_comment?place_id=1"

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetUserTest(APITestCase):
    def test_create_account(self):
        url = "http://127.0.0.1:8000/api/get_user?username=tom"
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        url_r = "http://127.0.0.1:8000/api/register"
        data_r = {
            "username": "tom",
            "email": "benny@gmail.com",
            "password": "unreveal"
        }

        response_r = self.client.post(url_r, data_r, format='json')
        self.assertEqual(response_r.status_code, status.HTTP_201_CREATED)

        url_p = "http://127.0.0.1:8000/api/addPlace"
        data_p = {
            "username": "tom",
            "latitude": "1234657865",
            "longitude": "456786754",
            "place": "caffee",
            "description": "best caffee in berlin",
            "label": "caffe;relax;fun",
        }

        response_p = self.client.post(url_p, data_p, format='json')
        self.assertEqual(response_p.status_code, status.HTTP_201_CREATED)


        url = "http://127.0.0.1:8000/api/get_user?username=tom"
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

