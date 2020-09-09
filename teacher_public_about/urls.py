from django.urls import path
from . import views

urlpatterns = [
    # teacher public - landing page
    path(
        "contrib/",
        views.teacher_public_landing_page,
        name="teacher_public_landing_page"
    ),
    # teacher public - course overviews
    path(
        "contrib/course/status/<str:language>/<str:speakers_language>/",
        views.teacher_public_course_status,
        name="teacher_public_course_status",
    ),
]
