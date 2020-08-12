from django.urls import path
from . import views

urlpatterns = [
    # Signup Page
    path("auth/signup/", views.signup, name="signup"),
    # Login Page
    path("auth/login/", views.login, name="login"),
    # Log out Page
    path("auth/logout/", views.logout, name="logout"),
    # Congrats Page
    path("auth/welcome/", views.welcome, name="welcome"),
]
