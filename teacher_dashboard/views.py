# Main Imports

# Django Imports
from django.shortcuts import render, get_object_or_404, HttpResponse
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.core.files import File
from django.contrib.auth.models import User

# My Module Imports
from .models import DashboardAnnouncament
from profile_settings.models import BasicUserProfile
from teacher_authentication.models import TeacherUserProfile
from utils.session_utils import get_current_user, get_current_user_profile
from utils.session_utils import get_current_teacher_user_profile


def teacher_dashboard_announcament(request):
    """
    in this view the teacher user can see their own course's announcaments
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

    # Getting all of the announcaments for the current teachers course
    filtered_announcaments = DashboardAnnouncament.objects.filter(
        course_language=current_teacher_profile.course_language,
        course_speakers_language=current_teacher_profile.course_speakers_language,
    ).order_by("-id")

    # create an announcament form processing
    if request.POST.get("teacher_announcament_submit_btn"):
        content = request.POST.get("announcament_content")

        new_announcament = DashboardAnnouncament(
            user=current_teacher_profile.user,
            teacher=current_teacher_profile,
            course_language=current_teacher_profile.course_language,
            course_speakers_language=current_teacher_profile.course_speakers_language,
            content=content
        )
        new_announcament.save()

    data = {
        "current_basic_user": current_basic_user,
        "current_basic_user_profile": current_basic_user_profile,
        "current_teacher_profile": current_teacher_profile,
        "filtered_announcaments": filtered_announcaments,
    }

    if "teacher_user_logged_in" in request.session:
        return render(request, "teacher_dashboard/announcament.html", data)
    else:
        return HttpResponseRedirect("/")
