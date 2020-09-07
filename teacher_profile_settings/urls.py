from django.urls import path
from . import views

urlpatterns = [
    # teacher public - landing page
    path(
        "teacher/profile/settings/edit_profile/",
        views.teacher_profile_settings_edit_profile,
        name="teacher_profile_settings_edit_profile"
    ),
]
