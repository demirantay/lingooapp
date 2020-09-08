from django.urls import path
from . import views

urlpatterns = [
    # Teacher Courses Overview
    path(
        "teacher/course/overview/",
        views.teacher_course_overview,
        name="teacher_course_overview"
    ),
    # Teacher Course Status
    path(
        "teacher/course/status/<str:language>/<str:speakers_language>/",
        views.teacher_course_status,
        name="teacher_course_status"
    ),
    # Teacher Course Status Update Form
    path(
        "teacher/course/status/update/",
        views.teacher_course_status_update,
        name="teacher_course_status_update"
    )
]
