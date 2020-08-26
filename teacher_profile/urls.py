from django.urls import path
from . import views

urlpatterns = [
    # Teacher Profile Overview
    path(
        "teacher/profile/",
        views.teacher_profile_overview,
        name="teacher_profile_overview"
    ),
    # Teacher Other User Overview
    path(
        "teacher/profile/<str:other_user_username>",
        views.teacher_profile_other_user_overview,
        name="teacher_profile_other_user_overview"
    ),
]
