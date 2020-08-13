from django.urls import path
from . import views

urlpatterns = [
    # Landing Page
    path('forum/', views.forum_landing_page, name="forum_landing_page"),
    # Forum Create
    path('forum/create/', views.forum_create, name="forum_create"),
    # Forum read
    path('forum/<int:post_id>/', views.forum_read, name="forum_read"),
    # Forum update
    path('forum/update/<int:post_id>/', views.forum_update, name="forum_update"),
]
