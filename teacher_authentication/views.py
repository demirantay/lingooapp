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


def teacher_apply(request):
    """
    In this view the users can fill the application form of becoming a teacher
    """
    # Deleting admin-typed user session
    # Deleting programmer-typed-user session
    # Deleting Teacher-typed user sessions

    # Get the current users
    current_basic_user = get_current_user(request, User, ObjectDoesNotExist)

    current_basic_user_profile = get_current_user_profile(
        request,
        User,
        BasicUserProfile,
        ObjectDoesNotExist
    )

    # Teacher Application Process
    empty_credentials = False
    is_above_13_years_old = True

    # if request.POST.get("")

        # create a new user without signup permissions with just email

    data = {
        "current_basic_user": current_basic_user,
        "current_basic_user_profile": current_basic_user_profile,
    }

    if current_basic_user == None:
        return HttpResponseRedirect("/auth/login/")
    else:
        return render(request, "teacher_authentication/apply.html", data)


def teacher_login(request):
    """
    """

    data = {

    }
    return render(request, "teacher_authentication/login.html", data)


def teacher_signup(request):
    """
    """

    data = {

    }
    return render(request, "teacher_authentication/signup.html", data)


# def teacher_logout(request):
# ...
