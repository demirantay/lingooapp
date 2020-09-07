# Main Imports

# Django Imports
from django.shortcuts import render, get_object_or_404, HttpResponse
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.core.files import File
from django.contrib.auth.models import User

# My Module Imports
from teacher_authentication.models import TeacherUserProfile
from profile_settings.models import BasicUserProfile
from utils.session_utils import get_current_user, get_current_user_profile
from utils.session_utils import get_current_teacher_user_profile
from utils.session_utils import get_other_user


def teacher_profile_overview(request):
    """
    in this view the teachers can see their own profile overview page
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

    data = {
        "current_basic_user": current_basic_user,
        "current_basic_user_profile": current_basic_user_profile,
        "current_teacher_profile": current_teacher_profile,
    }

    if "teacher_user_logged_in" in request.session:
        return render(request, "teacher_profile/overview.html", data)
    else:
        return HttpResponseRedirect("/")


def teacher_profile_other_user_overview(request, other_user_username):
    """
    in this view the user can see other teachers profiles
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

    # Getting the current user teacher profile
    current_teacher_profile = get_current_teacher_user_profile(
        request,
        User,
        TeacherUserProfile,
        ObjectDoesNotExist
    )

    # getting the other user's teacher profile
    other_basic_user = get_other_user(
        request,
        other_user_username,
        User,
        ObjectDoesNotExist
    )

    other_user_teacher_profile = TeacherUserProfile.objects.get(
        user=other_basic_user
    )

    data = {
        "current_basic_user": current_basic_user,
        "current_basic_user_profile": current_basic_user_profile,
        "current_teacher_profile": current_teacher_profile,
        "other_basic_user": other_basic_user,
        "other_user_teacher_profile": other_user_teacher_profile,
    }

    if "teacher_user_logged_in" in request.session:
        return render(request, "teacher_profile/other_user_overview.html", data)
    else:
        return HttpResponseRedirect("/")
