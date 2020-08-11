from django.urls import path
from . import views

urlpatterns = [
    # Profile Overview
    path("profile/settings/", views.profile_settings, name="profile_settings"),
    # Other User profile overview
]
