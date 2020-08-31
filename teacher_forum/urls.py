from django.urls import path
from . import views

urlpatterns = [
    # Teacher Forum Landing page
    path(
        "teacher/forum/<int:page>/",
        views.teacher_forum_landing_page,
        name="teacher_forum_landing_page"
    ),
    # Teacher forum create page
    path(
        "teacher/forum/create/",
        views.teacher_forum_create,
        name="teacher_forum_create"
    ),
    # Teacher forum read page
    path(
        "teacher/forum/read/<int:post_id>/",
        views.teacher_forum_read,
        name="teacher_forum_read"
    ),
    # Teacher forum update page
    path(
        "teacher/forum/update/<int:post_id>/",
        views.teacher_forum_update,
        name="teacher_forum_update"
    ),
]
