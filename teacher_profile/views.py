# Main Imports

# Django Imports
from django.shortcuts import render, get_object_or_404, HttpResponse
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.core.files import File
from django.contrib.auth.models import User

# My Module Imports
from profile_settings.models import BasicUserProfile
from utils.session_utils import get_current_user, get_current_user_profile


def teacher_profile_overview(request):
    """
    """

    data = {

    }
    return render(request, "teacher_profile/overview.html", data)


def teacher_profile_other_user_overview(request, other_user_username):
    """
    """

    data = {

    }
    return render(request, "teacher_profile/other_user_overview.html", data)
