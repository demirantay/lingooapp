from django.urls import path
from . import views

urlpatterns = [
    # Ranking Overview
    path(
        "ranking/overview/<int:page>/",
        views.ranking_overview,
        name="ranking_overview"
    ),
]
