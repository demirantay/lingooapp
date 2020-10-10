from django.urls import path
from . import views

urlpatterns = [
    # Create new bill page
    path(
        "voting/congress/bill/create/",
        views.basic_create_bill,
        name="basic_create_bill"
    ),
    # Bill post read page
    path(
        "voting/congress/bill/read/<int:bill_id>/",
        views.basic_read_bill,
        name="basic_read_bill",
    ),
    # Bill post update page
    path(
        "voting/congress/bill/update/<int:bill_id>/",
        views.basic_update_bill,
        name="basic_update_bill",
    ),
]
