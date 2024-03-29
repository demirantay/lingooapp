from django.urls import path
from . import views

urlpatterns = [
    # Learning Slides
    path(
        "vocab/learn/<str:cefr_level>/<str:course_language>/<str:speakers_langauge>/",
        views.basic_vocab_learn,
        name="basic_vocab_learn"
    ),
    # Learning Start Page
    path(
        "vocab/learn/start/<str:cefr_level>/<str:course_language>/<str:speakers_langauge>/",
        views.basic_vocab_learn_start,
        name="basic_vocab_learn_start"
    ),
    # Review page
    path(
        "vocab/review/<str:course_language>/<str:speakers_langauge>/",
        views.basic_vocab_review,
        name="basic_vocab_review"
    ),
]
