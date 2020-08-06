# Main Imports

# Django Imports
from django.shortcuts import render, get_object_or_404, HttpResponse
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.core.files import File
from django.contrib.auth.models import User

# My Module Imports


def index(request):
    """index will redirect the page to `learn` if user is logged in"""
    return render(request, "home/landing_page.html")


def under_construction(request):
    """under constrction page"""
    return render(request, "redirect_pages/under_construction.html")
