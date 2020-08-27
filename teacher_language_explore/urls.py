from django.urls import path
from . import views

urlpatterns = [
    # Teacher Courses Overview
    path(
        "teacher/course/overview/",
        views.teacher_course_overview,
        name="teacher_course_overview"
    ),
]
