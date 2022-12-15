from django.urls import path

from .views import CreateUser, LoginUser, LogoutUser,GetUserData,CreateRating
from .views import CreatePlace,WebHook,CreateComment,GetCommentsData,GetRatingData

urlpatterns = [
    path("register", CreateUser.as_view()),
    path("login", LoginUser.as_view()),
    path("logout", LogoutUser.as_view()),
    path("addPlace", CreatePlace.as_view()),
    path("addComment", CreateComment.as_view()),
    path("addRating", CreateRating.as_view()),
    path("get_comment", GetCommentsData.as_view()),
    path("get_rating", GetRatingData.as_view()),
    path("git_update", WebHook.as_view()),
    path("get_user", GetUserData.as_view()),
]
