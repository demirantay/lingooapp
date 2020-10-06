from django.urls import path
from . import views

urlpatterns = [
    # Create new bill page
    path(
        "voting/congress/bill/create",
        views.basic_create_bill,
        name="basic_create_bill"
    ),

]
