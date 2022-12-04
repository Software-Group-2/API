from django.shortcuts import render
from rest_framework import generics, status
from django.contrib.auth.models import User


from django.contrib.auth.hashers import check_password
from .serializers import CreateUserSerializer, LoginUserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.http import HttpResponse


# Create your views here.

class CreateUser(APIView):
    serializer_class = CreateUserSerializer

    def post(self, request, format=None):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            print(serializer.data)
            username = serializer.data.get('username')
            first_name = serializer.data.get('first_name')
            print(first_name)
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            queryset = User.objects.filter(username=username)
            queryset2 = User.objects.filter(email=email)

            if queryset.exists() or queryset2.exists():
                return Response({'Bad Request': 'Username or email already exists'}, status=status.HTTP_403_FORBIDDEN)
            else:
                user = User(username=username, first_name=first_name,
                            email=email, password=password)
                user.save()
                self.request.session['member_id'] = user.id
                return Response(CreateUserSerializer(user).data, status=status.HTTP_201_CREATED)

        return Response({'Bad Request': 'Username or email already exists'}, status=status.HTTP_403_FORBIDDEN)


class LoginUser(APIView):

    def post(self, request, format=None):
        #serializer = self.serializer_class(data=request.data)
        try:
            user = request.data['username']
            password = request.data['password']
            print(user, password)

            m = User.objects.get(username=user)
            #print(m.password == password)
            matchcheck = check_password(password, m.password)
            # print(matchcheck)
            if matchcheck:
                self.request.session['member_id'] = m.id
                return HttpResponse("You are logged in")
                return HttpResponseRedirect('/you-are-logged-in/')
            else:
                raise User.DoesNotExist
        except User.DoesNotExist:
            return Response({'Bad Request': 'username and password did not match'}, status=status.HTTP_403_FORBIDDEN)
        except:
            return Response({'Bad Request': 'Wrong input data'}, status=status.HTTP_400_BAD_REQUEST)


class LogoutUser(APIView):

    def post(self, request, format=None):
        try:
            del self.request.session['member_id']
        except KeyError:
            pass

        return HttpResponse("You're logged out.")
