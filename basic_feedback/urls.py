from django.urls import path
from . import views

urlpatterns = [
    # Language Explore
    path(
        "feedback/",
        views.basic_feedback_landing_page,
        name="basic_feedback_landing_page"
    ),

]
