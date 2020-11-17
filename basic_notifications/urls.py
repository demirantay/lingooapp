from django.urls import path
from . import views

urlpatterns = [
    # Notifications
    path("notifications/<int:page>/", views.notifications, name="notifications"),
]
