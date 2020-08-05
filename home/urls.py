from django.urls import path
from . import views

urlpatterns = [
    # Index of the webapp (landing page)
    path('', views.index, name="index"),
]
