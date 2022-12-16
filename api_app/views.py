from rest_framework import status
# from django.http import JsonResponse
# from django.http import HttpResponseRedirect
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
import git
from drf_yasg.utils import swagger_auto_schema

from django.core import management
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password, make_password
from .serializers import CreateUserSerializer, LoginUserSerializer
from .serializers import AddPlaceSerializer, AddCommentSerializer, PlaceViewSerializer
from .models import Place, Comment

# POST Requests


class CreateUser(APIView):
    serializer_class = CreateUserSerializer

    @swagger_auto_schema(responses={201: serializer_class(many=True)})
    def post(self, request, format=None):
        """ post request to register user"""

        serializer = self.serializer_class(data=request.data)
        # only username is unique email is not checked for uniqueness
        # maybe change this later
        if serializer.is_valid():
            print(serializer.data)
            username = serializer.data.get('username')
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            # queryset = User.objects.filter(username=username)
            # queryset2 = User.objects.filter(email=email)

            user = User(username=username, email=email,
                        password=make_password(password))
            user.save()
            self.request.session['member_id'] = user.id
            return Response(CreateUserSerializer(user).data,
                            status=status.HTTP_201_CREATED)

        return Response({'Bad Request': 'Username already exists or Invalid inputs'},
                        status=status.HTTP_403_FORBIDDEN)


class LoginUser(APIView):
    serializer_class = LoginUserSerializer

    @swagger_auto_schema(responses={200: serializer_class(many=True)})
    def post(self, request, format=None):
        """post request to login user"""
        # serializer = self.serializer_class(data=request.data)
        try:
            user = request.data['username']
            password = request.data['password']
            print(user, password)

            user_object = User.objects.get(username=user)
            # print(user_object.password == password)
            matchcheck = check_password(password, user_object.password)
            # print(matchcheck)
            if matchcheck:
                self.request.session['member_id'] = user_object.id
                return HttpResponse("You are logged in")
                # return HttpResponseRedirect('/you-are-logged-in/')

            return Response({'Bad Request': 'username and password did not match'},
                            status=status.HTTP_403_FORBIDDEN)

        except Exception as e:
            return Response({'Bad Request': 'Either user is not in Database or Invalid input'},
                            status=status.HTTP_400_BAD_REQUEST)


class LogoutUser(APIView):

    def post(self, request, format=None):
        """post request to logout"""
        try:
            del self.request.session['member_id']
        except KeyError:
            pass

        return HttpResponse("You're logged out.")


class CreatePlace(APIView):
    serializer_class = AddPlaceSerializer

    @swagger_auto_schema(responses={201: serializer_class(many=True)})
    def post(self, request, format=None):
        """ post request to create a place"""

        serializer = self.serializer_class(data=request.data)

        # only username is unique email is not checked for uniqueness
        # maybe change this later
        if serializer.is_valid():
            username = serializer.data.get('username')
            latitude = serializer.data.get('latitude')
            longitude = serializer.data.get('longitude')
            place = serializer.data.get('place')
            description = serializer.data.get('description')
            label = serializer.data.get('label')
            print(serializer.data)

            # queryset = User.objects.filter(username=username)
            # queryset2 = User.objects.filter(email=email)

            place_table = Place(username=username, latitude=latitude, longitude=longitude,
                                place=place, description=description, label=label)
            place_table.save()

            return Response(AddPlaceSerializer(place_table).data,
                            status=status.HTTP_201_CREATED)

        return Response({'Bad Request': 'Place: Invalid inputs'},
                        status=status.HTTP_403_FORBIDDEN)


class CreateComment(APIView):
    serializer_class = AddCommentSerializer

    @swagger_auto_schema(responses={201: serializer_class(many=True)})
    def post(self, request, format=None):
        """ post request to create a place"""

        serializer = self.serializer_class(data=request.data)

        # only username is unique email is not checked for uniqueness
        # maybe change this later
        if serializer.is_valid():
            post_id = serializer.data.get('post_id')
            sender_id = serializer.data.get('sender_id')
            comment = serializer.data.get('comment')
            print(serializer.data)

            # queryset = User.objects.filter(username=username)
            # queryset2 = User.objects.filter(email=email)

            commnet_table = Comment(
                post_id=post_id, sender_id=sender_id, comment=comment)
            commnet_table.save()

            return Response(AddCommentSerializer(commnet_table).data,
                            status=status.HTTP_201_CREATED)

        return Response({'Bad Request': 'Place: Invalid inputs'},
                        status=status.HTTP_403_FORBIDDEN)


class GetCommentsData(APIView):

    def get(self, request, format=None):
        """get request to get the comments of a post given the post id"""
        try:
            place_id = self.request.query_params.get('place_id')
            comment_places = Comment.objects.filter(post_id=place_id)
            comments = []
            for i in comment_places:
                comments.append(AddCommentSerializer(i).data)

            return Response({'comments': comments}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'Bad Request': 'No post with this id in Database'},
                            status=status.HTTP_404_NOT_FOUND)


class WebHook(APIView):
    swagger_schema = None

    def post(self, request, format=None):
        """ Webhook to pull the code from github to the backend server"""
        repo = git.Repo('./API')
        origin = repo.remotes.origin
        repo.create_head('main', origin.refs.main).set_tracking_branch(
            origin.refs.main).checkout()
        origin.pull()
        management.call_command('collectstatic', interactive=False)

        return '', 200


class GetUserData(APIView):

    def get(self, request, format=None):
        """get request to get the data of the user given his username"""
        try:
            username = self.request.query_params.get('username')
            user_object = User.objects.get(username=username)
            user_places = Place.objects.filter(username=username)
            places = []
            for i in user_places:
                places.append(PlaceViewSerializer(i).data)

            return Response(
                {
                    'id': user_object.id,
                    'username': user_object.username,
                    'email': user_object.email,
                    'places': places},
                status=status.HTTP_200_OK
            )

            # return Response({'id':self.request.session['member_id'],
            # 'username':user_object.username,
            # 'email':user_object.email,},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'Bad Request': 'No user with this username in Database'},
                            status=status.HTTP_404_NOT_FOUND)
