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


def teacher_forum_landing_page(request, page):
    """
    """

    data = {

    }
    return render(request, "teacher_forum/landing_page.html", data)


def teacher_forum_create(request):
    """
    """

    data = {

    }
    return render(request, "teacher_forum/create.html", data)


def teacher_forum_read(request, post_id):
    """
    """

    data = {

    }
    return render(request, "teacher_forum/read.html", data)


def teacher_forum_update(request, post_id):
    """
    """

    data = {

    }
    return render(request, "teacher_forum/update.html", data)
