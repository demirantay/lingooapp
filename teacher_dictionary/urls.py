from django.urls import path
from . import views

urlpatterns = [
    # teacher dictionary - explore page
    path(
        "teacher/dictionary/explore/",
        views.teacher_dictionary_explore,
        name="teacher_dictionary_explore"
    ),
]
