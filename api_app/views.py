from drf_yasg import openapi
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
import git
from django.forms.models import model_to_dict
from django.core.exceptions import ObjectDoesNotExist
from drf_yasg.utils import swagger_auto_schema
from django.core import management
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password, make_password
from rest_framework.exceptions import ValidationError
from .serializers import UserSerializer, LoginSerializer, ErrorResponseSerializer, \
    SuccessResponseSerializer, PlaceSerializer, CommentSerializer
from .models import Place, Comment


# POST Requests


class UserView(APIView):
    serializer_class = UserSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('username', openapi.IN_PATH, type=openapi.TYPE_STRING)],
        responses={201: serializer_class(many=True), 404: ErrorResponseSerializer}
    )
    def get(self, request, format=None):
        """get request to get the data of the user given his username"""
        try:
            username = self.request.query_params.get('username')
            user_object = User.objects.get(username=username)

            return Response(
                model_to_dict(user_object),
                status=status.HTTP_200_OK
            )

        except Exception as e:
            print(e)
            return Response({
                'error': 'Bad Request',
                'description': 'No register with this id in Database'
            }, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(request_body=UserSerializer,
                         responses={201: serializer_class(many=True),
                                    400: ErrorResponseSerializer,
                                    409: ErrorResponseSerializer})
    def post(self, request, format=None):
        """ post request to register user"""

        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            username = serializer.data.get('username')
            email = serializer.data.get('email')
            password = serializer.data.get('password')

            user = User(username=username, email=email,
                        password=make_password(password))
            user.save()
            self.request.session['member_id'] = user.id
            return Response(UserSerializer(user).data,
                            status=status.HTTP_201_CREATED)
        except ValidationError as e:
            print(e)
            return Response(
                {
                    'error': e.default_detail,
                    'description': e.detail
                },
                status=status.HTTP_409_CONFLICT if ['unique'] in e.get_codes().values()
                else status.HTTP_400_BAD_REQUEST)


class Login(APIView):
    serializer_class = LoginSerializer

    @swagger_auto_schema(request_body=LoginSerializer,
                         responses={200: SuccessResponseSerializer,
                                    401: ErrorResponseSerializer,
                                    404: ErrorResponseSerializer})
    def post(self, request, format=None):
        """post request to login user"""
        try:
            user = request.data['username']
            password = request.data['password']

            user_object = User.objects.get(username=user)
            match_check = check_password(password, user_object.password)
            if match_check:
                self.request.session['member_id'] = user_object.id
                return Response(
                    {
                        'message': 'OK',
                        'description': 'You are logged in'
                    },
                    status=status.HTTP_200_OK
                )
            raise AttributeError

        except AttributeError:
            return Response(
                {
                    'error': 'Bad Request',
                    'description': 'username and password did not match'
                },
                status=status.HTTP_401_UNAUTHORIZED)
        except ObjectDoesNotExist as e:
            print(e)
            return Response(
                {
                    'error': 'Not Found',
                    'description': e.args[0]
                },
                status=status.HTTP_404_NOT_FOUND)


class Logout(APIView):

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('username', openapi.IN_PATH, type=openapi.TYPE_STRING)],
        responses={200: SuccessResponseSerializer,
                   400: ErrorResponseSerializer})
    def post(self, request, format=None):
        """post request to logout"""
        try:
            del self.request.session['member_id']
            return Response(
                {
                    'message': 'OK',
                    'description': 'You are logged out'
                },
                status=status.HTTP_200_OK
            )
        except KeyError:
            return Response(
                {
                    'error': 'Bad Request',
                    'description': 'invalid username'
                },
                status=status.HTTP_400_BAD_REQUEST)


class PlaceView(APIView):
    serializer_class = PlaceSerializer

    @swagger_auto_schema(request_body=PlaceSerializer,
                         responses={201: PlaceSerializer,
                                    400: ErrorResponseSerializer
                                    })
    def post(self, request, format=None):
        """ post request to create a place"""

        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            User.objects.get(username=serializer.data.get('username'))
            username = serializer.data.get('username')
            latitude = serializer.data.get('latitude')
            longitude = serializer.data.get('longitude')
            name = serializer.data.get('name')
            description = serializer.data.get('description')
            label = serializer.data.get('label')

            place_table = Place(
                username=username,
                latitude=latitude,
                longitude=longitude,
                name=name,
                description=description,
                label=label
            )
            place_table.save()

            return Response(PlaceSerializer(place_table).data,
                            status=status.HTTP_201_CREATED)

        except ObjectDoesNotExist as e:
            print(e)
            return Response(
                {
                    'error': 'Username Not Found',
                    'description': e.args[0]
                },
                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response(
                {
                    'error': 'Bad Request',
                    'description': 'Invalid inputs'
                }, status=status.HTTP_400_BAD_REQUEST)


class CommentView(APIView):
    serializer_class = CommentSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('place_id', openapi.IN_PATH, type=openapi.TYPE_STRING)],
        responses={201: serializer_class(many=True), 404: ErrorResponseSerializer}
    )
    def get(self, request, format=None):
        """get request to get the comments of a post given the post id"""
        try:
            place_id = self.request.query_params.get('place_id')
            comment_places = Comment.objects.filter(place_id=place_id)
            Place.objects.get(id__exact=place_id)
            if not comment_places:
                raise ObjectDoesNotExist
            comments = []
            for i in comment_places:
                comments.append(CommentSerializer(i).data)

            return Response(
                comments,
                status=status.HTTP_200_OK
            )
        except ObjectDoesNotExist as e:
            print(e)
            return Response(
                {
                    'error': 'Not Found',
                    'description': 'There is no comment found for this place'
                },
                status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({
                'error': 'Bad Request',
                'description': 'No register with this id in Database'
            }, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(request_body=CommentSerializer,
                         responses={201: serializer_class(many=True), 403: ErrorResponseSerializer})
    def post(self, request, format=None):
        """ post request to create a place"""

        serializer = self.serializer_class(data=request.data)

        try:
            serializer.is_valid()
            place_id = serializer.data.get('place_id')
            username = serializer.data.get('username')
            comment = serializer.data.get('comment')

            User.objects.get(username=username)
            Place.objects.get(id=place_id)

            comment_table = Comment(
                place_id=place_id, username=username, comment=comment)
            comment_table.save()

            return Response(CommentSerializer(comment_table).data,
                            status=status.HTTP_201_CREATED)

        except ObjectDoesNotExist as e:
            print(e)
            return Response(
                {
                    'error': 'Not Found',
                    'description': e.args[0]
                },
                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response(
                {
                    'error': 'Bad Request',
                    'description': 'Invalid inputs'
                }, status=status.HTTP_400_BAD_REQUEST)


class WebHook(APIView):
    swagger_schema = None

    @staticmethod
    def post(request, format=None):
        """ Webhook to pull the code from GitHub to the backend server"""
        repo = git.Repo('./API')
        origin = repo.remotes.origin
        repo.create_head('main', origin.refs.main).set_tracking_branch(
            origin.refs.main).checkout()
        origin.pull()
        management.call_command('collectstatic', interactive=False)

        return '', 200
