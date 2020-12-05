from django.urls import path
from . import views

urlpatterns = [
    # Ranking Overview
    path(
        "ranking/overview/<int:page>/",
        views.ranking_overview,
        name="ranking_overview"
    ),
    # Category Ranking Page
    path(
        "ranking/<str:language>/<int:page>/",
        views.category_ranking,
        name="category_ranking"
    ),

]
