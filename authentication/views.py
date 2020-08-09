# Main Imports

# Django Imports
from django.shortcuts import render, get_object_or_404, HttpResponse
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.core.files import File
from django.contrib.auth.models import User

# My Module Imports


def signup(request):
    """foo"""

    data = {}
    return render(request, "about/about.html", data)


def login(request):
    """foo"""

    data = {}
    return render(request, "about/about.html", data)


def congrats(request):
    """foo"""

    data = {}
    return render(request, "about/about.html", data)


def logout(request):
    """foo"""

    data = {}
    return render(request, "about/about.html", data)
