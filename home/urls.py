from django.urls import path
from . import views

urlpatterns = [
    # Index of the webapp (landing page)
    path('', views.index, name="index"),
    # Under Construction
    path('under_construction/', views.under_construction, name="under_construction"),
    # error_404
    path('404/', views.error_404, name="error_404"),
]
