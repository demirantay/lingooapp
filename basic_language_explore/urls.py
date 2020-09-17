from django.urls import path
from . import views

urlpatterns = [
    # Language Explore
    path("language/explore/", views.basic_language_explore, name="basic_language_explore"),
    # Specific Language Page
    path(
        "language/explore/info/<str:course_language>/<str:speakers_language>/",
        views.basic_language_explore_info,
        name="basic_language_explore_info"
    ),
]
