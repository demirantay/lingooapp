# Main Imports

# Django Imports
from django.shortcuts import render, get_object_or_404, HttpResponse
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.core.files import File
from django.contrib.auth.models import User

# My Module Imports
from profile_settings.models import BasicUserProfile
from utils.session_utils import get_current_user, get_current_user_settings


def index(request):
    """index will redirect the page to `learn` if user is logged in"""
    # Deleting any sessions regarding top-tier type of users
    # session.pop("programmer_username", None)  <-- these are flask change it
    # session.pop("programmer_logged_in", None) <-- these are flask change it
    # admin user session pop
    # admin user session pop

    # Get the current users
    current_basic_user = get_current_user(request, User, ObjectDoesNotExist)

    current_basic_user_settings = get_current_user_settings(
        request,
        User,
        BasicUserProfile,
        ObjectDoesNotExist
    )

    if current_basic_user == None:
        return render(request, "home/landing_page.html")
    else:
        return render(request, "home/placeholder_home.html")


def under_construction(request):
    """under constrction page"""
    return render(request, "redirect_pages/under_construction.html")
