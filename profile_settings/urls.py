from django.urls import path
from . import views

urlpatterns = [
    # Profile Overview
    path("profile/settings/edit_profile/", views.profile_settings_edit_profile, name="profile_settings_edit_profile"),
    # Other User profile overview
]
