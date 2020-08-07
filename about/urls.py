from django.urls import path
from . import views

urlpatterns = [
    # About Us Page
    path('about/', views.about, name="about"),
    #
]
