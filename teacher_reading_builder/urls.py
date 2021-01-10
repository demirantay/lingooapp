from django.urls import path
from . import views

urlpatterns = [
    # teacher reading - build page
    path(
        "teacher/reading/build/",
        views.teacher_reading_build,
        name="teacher_reading_build"
    ),
]
