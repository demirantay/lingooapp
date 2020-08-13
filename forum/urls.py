from django.urls import path
from . import views

urlpatterns = [
    # Landing Page
    path('forum/', views.forum_landing_page, name="forum_landing_page"),
    # Forum Create
    path('forum/create/', views.forum_create, name="forum_create"),
]
