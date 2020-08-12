# Main Imports

# Django Imports
from django.shortcuts import render, get_object_or_404, HttpResponse
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.core.files import File
from django.contrib.auth.models import User

# My Module Imports


def signup(request):
    """users can use this page to signup to the platform and create accounts"""

    # Signup Form Processing

    data = {}
    return render(request, "authentication/signup.html", data)


def login(request):
    """users can use this page to login to the platform"""

    data = {}
    return render(request, "authentication/login.html", data)


def logout(request):
    """users can use this page to logout of the site"""

    data = {}
    return render(request, "redirect_pages/error_400.html", data)


def welcome(request):
    """users use this inital congrats page to choose their first language"""

    data = {}
    return render(request, "authentication/welcome.html", data)
