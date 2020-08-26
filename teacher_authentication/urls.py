from django.urls import path
from . import views

urlpatterns = [
    # Contributor public apply
    path("contrib/apply/", views.teacher_apply, name="teacher_apply"),
]
