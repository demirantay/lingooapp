from django.urls import path
from . import views

urlpatterns = [
    # Profile Overview
    path("profile/", views.profile_overview, name="profile_overview")
    # Other User profile overview

]
