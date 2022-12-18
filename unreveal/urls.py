from django.urls import path

from .views import UserView, Login, Logout
from .views import PlaceView, WebHook, CommentView, RatingView

urlpatterns = [
    path("user", UserView.as_view()),
    path("login", Login.as_view()),
    path("logout", Logout.as_view()),
    path("place", PlaceView.as_view()),
    path("comment", CommentView.as_view()),
    path("git_update", WebHook.as_view()),
    path("rating", RatingView.as_view()),
]
