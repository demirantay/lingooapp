from django.urls import path
from . import views

urlpatterns = [
    # Signup Page
    path("auth/signup/", views.signup, name="signup"),
    # Login Page
    path("auth/login/", views.login, name="login"),
    # Congrats Page
    path("auth/congrats/", views.congrats, name="congrats"),
    # Log out Page
    path("auth/logout/", views.logout, name="logout"),
]
