from django.urls import path
from . import views

urlpatterns = [
    # Learning Slides
    path("vocab/learn/", views.basic_vocab_learn, name="basic_vocab_learn"),
    # Learning Start Page
    path("vocab/learn/start/", views.basic_vocab_learn_start, name="basic_vocab_learn_start"),
]
