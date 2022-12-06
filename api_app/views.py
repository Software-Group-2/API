from rest_framework import status
#from django.http import JsonResponse
#from django.http import HttpResponseRedirect
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response


from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password,make_password
from .serializers import CreateUserSerializer,LoginUserSerializer




# Create your views here.

class CreateUser(APIView):
    serializer_class = CreateUserSerializer

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
            #queryset = User.objects.filter(username=username)
            #queryset2 = User.objects.filter(email=email)

            user = User(username=username,email=email, password=make_password(password))
            user.save()
            self.request.session['member_id'] = user.id
            return Response(CreateUserSerializer(user).data,
                            status=status.HTTP_201_CREATED)

        return Response({'Bad Request': 'Username already exists or Invalid inputs'},
        status=status.HTTP_403_FORBIDDEN)


class LoginUser(APIView):
    serializer_class = LoginUserSerializer

    def post(self, request, format=None):
        """post request to login user"""
        #serializer = self.serializer_class(data=request.data)
        try:
            user = request.data['username']
            password = request.data['password']
            print(user, password)

            user_object = User.objects.get(username=user)
            #print(user_object.password == password)
            matchcheck = check_password(password, user_object.password)
            # print(matchcheck)
            if matchcheck:
                self.request.session['member_id'] = user_object.id
                return HttpResponse("You are logged in")
                #return HttpResponseRedirect('/you-are-logged-in/')
        
            return Response({'Bad Request': 'username and password did not match'},
                        status=status.HTTP_403_FORBIDDEN)

        except:
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
