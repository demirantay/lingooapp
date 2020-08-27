from django.urls import path
from . import views

urlpatterns = [
    # teacher public - landing page
    path(
        "teacher/dashboard/announcament/",
        views.teacher_dashboard_announcament,
        name="teacher_dashboard_announcament"
    ),
]
