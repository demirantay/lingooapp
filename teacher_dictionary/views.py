# Main Imports

# Django Imports
from django.shortcuts import render, get_object_or_404, HttpResponse
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

# My Module Imports
from profile_settings.models import BasicUserProfile
from teacher_authentication.models import TeacherUserProfile
from utils.session_utils import get_current_user, get_current_user_profile
from utils.session_utils import get_current_teacher_user_profile

from .models import TeacherDictionary


def teacher_dictionary_explore(request):
    """
    in this view the teachers can see the listings of all of the dictionaries
    """
    # Deleting admin-typed user session
    # Deleting programmer-typed-user session

    # Get the current users
    current_basic_user = get_current_user(request, User, ObjectDoesNotExist)

    current_basic_user_profile = get_current_user_profile(
        request,
        User,
        BasicUserProfile,
        ObjectDoesNotExist
    )

    # Getting the teacher profile
    current_teacher_profile = get_current_teacher_user_profile(
        request,
        User,
        TeacherUserProfile,
        ObjectDoesNotExist
    )

    # Get all of the dictionaries
    try:
        all_dictionaries = TeacherDictionary.objects.all()
    except ObjectDoesNotExist:
        all_dictionaries = None

    data = {
        "current_basic_user": current_basic_user,
        "current_basic_user_profile": current_basic_user_profile,
        "current_teacher_profile": current_teacher_profile,
        "all_dictionaries": all_dictionaries,
    }

    if "teacher_user_logged_in" in request.session:
        return render(request, "teacher_dictionary/explore.html", data)
    else:
        return HttpResponseRedirect("/")


def teacher_dictionary_build(request):
    """

    """

    data = {

    }

    return render(request, "teacher_dictionary/build.html", data)


def teacher_dictionary_update(request, id):
    """

    """

    data = {

    }

    return render(request, "teacher_dictionary/update.html", data)
