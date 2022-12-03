from django.shortcuts import render

# Create your views here.

class LogoutUser(APIView):

    def post(self,request,format = None):
        try:
            del self.request.session['member_id']
        except KeyError:
            pass
        
        return HttpResponse("You're logged out.")
