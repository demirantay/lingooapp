# Main Imports

# Django Imports
from django.shortcuts import render, get_object_or_404, HttpResponse
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.core.files import File
from django.contrib.auth.models import User

# My Module Imports
from profile_settings.models import BasicUserProfile
from teacher_authentication.models import TeacherUserProfile
from .models import TeacherLanguageCourse
from utils.session_utils import get_current_user, get_current_user_profile
from utils.session_utils import get_current_teacher_user_profile


def teacher_course_overview(request):
    """
    in this view the teachers can see a overview of the languages courses
    that are being developed
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

    # Getting all the language courses
    try:
        all_teacher_courses = TeacherLanguageCourse.objects.all()
    except ObjectDoesNotExist:
        all_teacher_courses = None

    # Getting course contributers count
    course_contributers = {}
    for course in all_teacher_courses:
        contributers = TeacherUserProfile.objects.filter(
            course_language=course.course_language,
            course_speakers_language=course.course_speakers_language
        )
        contributer_count = 0
        for contributer in contributers:
            contributer_count += 1
        course_contributers[course.id] = contributer_count

    data = {
        "current_basic_user": current_basic_user,
        "current_basic_user_profile": current_basic_user_profile,
        "current_teacher_profile": current_teacher_profile,
        "all_teacher_courses": all_teacher_courses,
        "course_contributers": course_contributers,
    }

    if "teacher_user_logged_in" in request.session:
        return render(request, "teacher_language_explore/course_overview.html", data)
    else:
        return HttpResponseRedirect("/")


def teacher_course_status(request, language, speakers_language):
    """
    in this view the teachers can see the status of the other courses
    """

    data = {

    }
    return render(request, "teacher_language_explore/course_status.html", data)


def teacher_course_status_update(request):
    """
    """

    data = {

    }
    return render(request, "teacher_language_explore/course_status_update_form.html", data)
