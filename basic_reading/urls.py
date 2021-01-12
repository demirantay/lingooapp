from django.urls import path
from . import views

urlpatterns = [
    # Learning Start
    path(
        "reading/learn/start/",
        views.basic_reading_learn_start,
        name="basic_reading_learn_start"
    ),

    # Learning Lesson
    path(
        "reading/learn/",
        views.basic_reading_learn,
        name="basic_reading_learn"
    ),
]
