import uuid

from rest_framework import status
from rest_framework.test import APITestCase
from api_app.models import User


class Login(APITestCase):
    def test_login(self):
        base_url = "http://127.0.0.1:8000/api"
        register_data = {
            "username": "benny22",
            "email": "benny@gmail.com",
            "password": "unreveal"
        }
        self.client.post(f'{base_url}/user', register_data, format="json")

        data = {
            "username": "benny22",
            "password": "unreveal"
        }
        response = self.client.post(f'{base_url}/login', data, format="json")

        self.assertEqual(
            response.content, b'{"message":"OK","description":"You are logged in"}')

    def test_login_user_not_found(self):
        url = "http://127.0.0.1:8000/api/login"

        data = {
            "username": "benny22",
            "password": "unreveal"
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_login_wrong_password(self):
        base_url = "http://127.0.0.1:8000/api"
        register_data = {
            "username": "benny22",
            "email": "benny@gmail.com",
            "password": "password"
        }
        self.client.post(f'{base_url}/user', register_data, format="json")

        data = {
            "username": "benny22",
            "password": "anotherpassword"
        }
        response = self.client.post(f'{base_url}/login', data, format="json")

        self.assertEqual(
            response.content, b'{"error":"Bad Request","description":"username and password did not match"}')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class Logout(APITestCase):
    def test_logout(self):
        base_url = "http://127.0.0.1:8000/api"
        register_data = {
            "username": "benny22",
            "email": "benny@gmail.com",
            "password": "unreveal"
        }
        self.client.post(f'{base_url}/user', register_data, format="json")

        data = {
            "username": "benny22",
            "password": "unreveal"
        }
        self.client.post(f'{base_url}/login', data, format="json")

        response = self.client.post(f'{base_url}/logout', {}, format='json')
        self.assertEqual(response.content, b'{"message":"OK","description":"You are logged out"}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fail_logout(self):
        url = "http://127.0.0.1:8000/api/logout"

        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.content,
                         b'{"error":"Bad Request","description":"invalid username"}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class Place(APITestCase):
    def test_create_place(self):
        base_url = "http://127.0.0.1:8000/api"
        data = {
            "username": "tom",
            "email": "benny@gmail.com",
            "password": "unreveal"
        }

        self.client.post(f'{base_url}/user', data, format='json')

        data = {
            "username": "tom",
            "latitude": "1234657865",
            "longitude": "456786754",
            "name": "caffee",
            "description": "best caffee in berlin",
            "label": "caffe;relax;fun",
        }

        response = self.client.post(f'{base_url}/place', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_bad_request_create_place_user_do_not_exists(self):
        base_url = "http://127.0.0.1:8000/api"
        data = {
            "username": "tom",
            "latitude": "1234657865",
            "longitude": "456786754",
            "name": "caffee",
            "description": "best caffee in berlin",
            "label": "caffe;relax;fun",
        }

        response = self.client.post(f'{base_url}/place', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class CommentTest(APITestCase):
    def test_create_comment(self):
        base_url = "http://127.0.0.1:8000/api"
        data = {
            "username": "tom",
            "email": "benny@gmail.com",
            "password": "unreveal"
        }

        self.client.post(f'{base_url}/user', data, format='json')

        data = {
            "username": "tom",
            "latitude": "1234657865",
            "longitude": "456786754",
            "name": "caffee",
            "description": "best caffee in berlin",
            "label": "caffe;relax;fun",
        }

        response = self.client.post(f'{base_url}/place', data, format='json')

        data = {
            "place_id": response.data['id'],
            "username": "tom",
            "comment": "Hi im here for testing",
        }

        response = self.client.post(f'{base_url}/comment', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_bad_request_create_comment_user_do_not_exists(self):
        base_url = "http://127.0.0.1:8000/api"

        data = {
            "username": "tom",
            "email": "benny@gmail.com",
            "password": "unreveal"
        }

        self.client.post(f'{base_url}/user', data, format='json')

        data = {
            "username": "tom",
            "latitude": "1234657865",
            "longitude": "456786754",
            "name": "caffee",
            "description": "best caffee in berlin",
            "label": "caffe;relax;fun",
        }

        response = self.client.post(f'{base_url}/place', data, format='json')

        data = {
            "place_id": response.data['id'],
            "username": "marcus",
            "comment": "Hi im here for testing",
        }

        response = self.client.post(f'{base_url}/comment', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.content,
                         b'{"error":"Not Found","description":"User matching query does not exist."}')

    def test_bad_request_create_comment_place_do_not_exists(self):
        base_url = "http://127.0.0.1:8000/api"

        data = {
            "username": "tom",
            "email": "benny@gmail.com",
            "password": "unreveal"
        }

        self.client.post(f'{base_url}/user', data, format='json')

        data = {
            "place_id": uuid.uuid1(),
            "username": "tom",
            "comment": "Hi im here for testing",
        }

        response = self.client.post(f'{base_url}/comment', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.content,
                         b'{"error":"Not Found","description":"Place matching query does not exist."}')

    def test_get_comment(self):
        base_url = "http://127.0.0.1:8000/api"
        data = {
            "username": "tom",
            "email": "benny@gmail.com",
            "password": "unreveal"
        }

        self.client.post(f'{base_url}/user', data, format='json')

        data = {
            "username": "tom",
            "latitude": "1234657865",
            "longitude": "456786754",
            "name": "caffee",
            "description": "best caffee in berlin",
            "label": "caffe;relax;fun",
        }

        response = self.client.post(f'{base_url}/place', data, format='json')

        data = {
            "place_id": response.data['id'],
            "username": "tom",
            "comment": "Hi im here for testing",
        }

        self.client.post(f'{base_url}/comment', data, format='json')

        response = self.client.get(
            f'{base_url}/comment?place_id={response.data["id"]}', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_not_found_get_non_existent_comment(self):
        base_url = "http://127.0.0.1:8000/api"
        data = {
            "username": "tom",
            "email": "benny@gmail.com",
            "password": "unreveal"
        }

        self.client.post(f'{base_url}/user', data, format='json')

        data = {
            "username": "tom",
            "latitude": "1234657865",
            "longitude": "456786754",
            "name": "caffee",
            "description": "best caffee in berlin",
            "label": "caffe;relax;fun",
        }

        response = self.client.post(f'{base_url}/place', data, format='json')

        response = self.client.get(
            f'{base_url}/comment?place_id={response.data["id"]}', format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestUser(APITestCase):

    def test_user_not_found(self):
        url = "http://127.0.0.1:8000/api/user?username=tom"
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_user(self):
        url = "http://127.0.0.1:8000/api/user"
        data = {
            "username": "tom",
            "email": "benny@gmail.com",
            "password": "unreveal"
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(User.objects.filter(username='tom')), 1)

    def test_bad_request_create_user_wrong_email(self):
        url = "http://127.0.0.1:8000/api/user"
        data = {
            "username": "tom",
            "email": "bennygmail.com",
            "password": "unreveal"
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_user(self):
        url = "http://127.0.0.1:8000/api/user"
        data = {
            "username": "tom",
            "email": "benny@gmail.com",
            "password": "unreveal"
        }
        self.client.post(url, data, format='json')
        response = self.client.get(f'{url}?username=tom', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_conflict_with_duplicated_user(self):
        url = "http://127.0.0.1:8000/api/user"
        data = {
            "username": "benny22",
            "email": "benny@gmail.com",
            "password": "unreveal"
        }

        self.client.post(url, data, format='json')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
