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


def teacher_profile_settings_edit_profile(request):
    """
    the teacher can change their settings in this view
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

    # Change user settings form processing
    empty_credentials = False
    invalid_credentials = False

    if request.POST.get("teacher_edit_profile_submit_btn"):
        profile_photo = request.FILES.get("profile_photo")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        bio = request.POST.get("bio")
        location = request.POST.get("location")
        occupation = request.POST.get("occupation")
        personal_url = request.POST.get("personal_link")

        # update the teacer profile
        current_teacher_profile.profile_photo = profile_photo
        current_teacher_profile.first_name = first_name
        current_teacher_profile.last_name = last_name
        current_teacher_profile.bio = bio
        current_teacher_profile.location = location
        current_teacher_profile.occupation = occupation
        current_teacher_profile.personal_url = personal_url
        current_teacher_profile.save()
        return HttpResponseRedirect("/teacher/profile/")

    data = {
        "current_basic_user": current_basic_user,
        "current_basic_user_profile": current_basic_user_profile,
        "current_teacher_profile": current_teacher_profile,
    }

    if "teacher_user_logged_in" in request.session:
        return render(request, "teacher_profile_settings/edit_profile.html", data)
    else:
        return HttpResponseRedirect("/")
