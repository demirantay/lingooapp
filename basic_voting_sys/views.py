# Main Imports
import json

# Django Imports
from django.shortcuts import render, get_object_or_404, HttpResponse
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.core.files import File
from django.contrib.auth.models import User

# My Module ImportsImports


def basic_create_bill(request):
    """

    """

    data = {

    }

    return render(request, "basic_voting_sys/create_bill.html", data)


def basic_read_bill(request, bill_id):
    """

    """

    data = {

    }

    return render(request, "basic_voting_sys/read_bill.html", data)


def basic_update_bill(request, bill_id):
    """

    """

    data = {

    }

    return render(request, "basic_voting_sys/update_bill.html", data)


def basic_bill_landing_page(request):
    """
    """

    data = {

    }

    return render(request, "basic_voting_sys/landing_page.html", data)


def basic_bill_passed_page(request):
    """
    """

    data = {

    }

    return render(request, "basic_voting_sys/passed_page.html", data)


def basic_bill_shelved_page(request):
    """
    """

    data = {

    }

    return render(request, "basic_voting_sys/shelved_page.html", data)


def basic_bill_new_page(request):
    """
    """

    data = {

    }

    return render(request, "basic_voting_sys/new_page.html", data)
