from django.urls import path
from .views import CreateUser, LoginUser, LogoutUser,WebHook

urlpatterns = [
    path("register", CreateUser.as_view()),
    path("login", LoginUser.as_view()),
    path("logout", LogoutUser.as_view()),
    path("git_update", WebHook.as_view()),
]
