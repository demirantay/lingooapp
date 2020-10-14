from django.urls import path
from . import views

urlpatterns = [
    # Language Explore
    path(
        "feedback/",
        views.basic_feedback_landing_page,
        name="basic_feedback_landing_page"
    ),
    # Feedback read page
    path(
        "feedback/read/<int:feedback_id>/",
        views.basic_feedback_read,
        name="basic_feedback_read"
    ),

]
