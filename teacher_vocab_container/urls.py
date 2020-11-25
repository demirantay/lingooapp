from django.urls import path
from . import views

urlpatterns = [
    # teacher vocab container OVERVIEW
    path(
        "teacher/vocab/container/overview/",
        views.teacher_vocab_container_overview,
        name="teacher_vocab_container_overview"
    ),
    # teacher vocab container EDIT WORD
    path(
        "teacher/vocab/container/edit/<int:word_id>/<str:word>/",
        views.teacher_vocab_container_edit,
        name="teacher_vocab_container_edit"
    ),
    # teacher vocab container ADD SOUND
    path(
        "teacher/vocab/container/sound/<int:word_id>/",
        views.teacher_vocab_container_add_sound,
        name="teacher_vocab_container_add_sound"
    ),
]
