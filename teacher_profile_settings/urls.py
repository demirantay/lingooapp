from django.urls import path
from . import views

urlpatterns = [
    # teacher public - landing page
    path(
        "teacher/profile/settings/edit_profile/",
        views.teacher_profile_settings_edit_profile,
        name="teacher_profile_settings_edit_profile"
    ),
    # teacher public - course overviews
    path(
        "teacher/profile/settings/change_password/",
        views.teacher_profile_settings_change_password,
        name="teacher_profile_settings_change_password",
    ),
]
