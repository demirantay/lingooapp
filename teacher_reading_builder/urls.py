from django.urls import path
from . import views

urlpatterns = [
    # teacher reading - build page
    path(
        "teacher/reading/build/",
        views.teacher_reading_build,
        name="teacher_reading_build"
    ),

    # teacher reading - update page
    path(
        "teacher/reading/update/<int:id>/",
        views.teacher_reading_update,
        name="teacher_reading_update"
    ),

    # teacher reading - update page
    path(
        "teacher/reading/build/sentence/",
        views.teacher_reading_add_sentence,
        name="teacher_reading_add_sentence"
    ),
]
