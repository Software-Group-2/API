from django.urls import path
from .views import CreateUser, LoginUser, LogoutUser,CreatePlace

urlpatterns = [
    path("register", CreateUser.as_view()),
    path("login", LoginUser.as_view()),
    path("logout", LogoutUser.as_view()),
    path("addPlace", CreatePlace.as_view())
]
