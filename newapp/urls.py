from django.urls import path

from . import views

app_name = "flowih"
urlpatterns = [
    path("", views.index, name="index"),
    path("signup", views.signup, name="signup"),
    path("auth", views.controllerSignup, name="auth"),
    path("signin", views.signin, name="signin"),
    path("authSignin", views.controllerSignin, name="authSignin"),
    path("user/<str:username>", views.userView, name="details"),
    path("logout", views.deleting_cookie, name="logout"),
    path("vote/<int:choice_id>", views.vote, name="vote"),
    path("user/<str:username>/newchoice", views.newchoice, name="newchoice")
]