from django.urls import path
from . import views

urlpatterns = [
    # Language Explore
    path("language/explore/", views.basic_language_explore, name="basic_language_explore"),
]
