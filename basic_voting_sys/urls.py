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
    # Bills landing page
    path(
        "voting/congress/<int:page>/",
        views.basic_bill_landing_page,
        name="basic_bill_landing_page",
    ),
    # Bills passed bills page
    path(
        "voting/congress/passed/<int:page>/",
        views.basic_bill_passed_page,
        name="basic_bill_passed_page",
    ),
    # Bills shelved bills page
    path(
        "voting/congress/shelved/<int:page>/",
        views.basic_bill_shelved_page,
        name="basic_bill_shelved_page",
    ),
    # Bills shelved bills page
    path(
        "voting/congress/new/<int:page>/",
        views.basic_bill_new_page,
        name="basic_bill_new_page",
    ),
]
