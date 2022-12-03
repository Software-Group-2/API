from django.shortcuts import render

# Create your views here.


class LoginUser(APIView):

    def post(self,request,format = None):
        #serializer = self.serializer_class(data=request.data)
        try:
            user = request.data['username']
            password = request.data['password']
            print(user,password)
            
            m = User.objects.get(username=user)
            matchcheck = check_password(password,m.password)
            if matchcheck:
                self.request.session['member_id'] = m.id
                return HttpResponse("You are logged in")
                return HttpResponseRedirect('/you-are-logged-in/')
            else:
                raise User.DoesNotExist
        except User.DoesNotExist:
            return HttpResponse("Your username and password didn't match.")
        except:
            return Response({'Bad Request': 'User already exists'}, status=status.HTTP_403_FORBIDDEN)

        


class LogoutUser(APIView):

    def post(self,request,format = None):
        try:
            del self.request.session['member_id']
        except KeyError:
            pass
        
        return HttpResponse("You're logged out.")
