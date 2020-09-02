from django.urls import path
from . import views

urlpatterns = [
    # Contributor public apply
    path("contrib/apply/", views.teacher_apply, name="teacher_apply"),
    # Thanks for Applying page
    path("contrib/apply/thanks/", views.application_thank_you_page, name="application_thank_you_page"),
    # Teacher login gate
    path("teacher/login/", views.teacher_login, name="teacher_login"),
    # Tecaher signup gate
    path("teacher/signup/", views.teacher_signup, name="teacher_signup"),
]
