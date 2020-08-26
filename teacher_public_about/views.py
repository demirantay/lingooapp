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


def teacher_public_landing_page(request):
    """
    """

    data = {

    }
    return render(request, "teacher_public_about/landing_page.html", data)


def teacher_public_course_status(request, language, language_for):
    """
    """

    data = {

    }
    return render(request, "teacher_public_about/course_status.html", data)
