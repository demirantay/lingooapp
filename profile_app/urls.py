from django.urls import path
from . import views

urlpatterns = [
    # Profile Overview
    path("profile/", views.profile_overview, name="profile_overview"),
    # Other User profile overview
    path(
        "profile/<str:other_user_username>/",
        views.other_user_profile_overview,
        name="other_user_profile_overview"
    ),
]
