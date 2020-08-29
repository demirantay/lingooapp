from django.urls import path
from . import views

urlpatterns = [
    # teacher vocab container OVERVIEW
    path(
        "teacher/vocab/container/overview/",
        views.teacher_vocab_container_overview,
        name="teacher_vocab_container_overview"
    ),
]
