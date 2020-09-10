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
from teacher_language_explore.models import TeacherLanguageCourse
from teacher_language_explore.models import CourseStatusUpdate
from utils.session_utils import get_current_user, get_current_user_profile
from utils.access_control import delete_teacher_user_session


def teacher_public_landing_page(request):
    """
    in this view the basic users of the site can see how to development of
    language courses are going on.
    """
    # Deleting any sessions regarding top-tier type of users
    # session.pop("programmer_username", None)  <-- these are flask change it
    # session.pop("programmer_logged_in", None) <-- these are flask change it
    # admin user session pop
    # admin user session pop

    # ACCESS CONTROL
    delete_teacher_user_session(request)

    # Get the current users
    current_basic_user = get_current_user(request, User, ObjectDoesNotExist)

    current_basic_user_profile = get_current_user_profile(
        request,
        User,
        BasicUserProfile,
        ObjectDoesNotExist
    )

    # Getting all the language courses that are being developed
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
        "all_teacher_courses": all_teacher_courses,
        "course_contributers": course_contributers,
    }

    if current_basic_user == None:
        return HttpResponseRedirect("/auth/login/")
    else:
        return render(request, "teacher_public_about/landing_page.html", data)


def teacher_public_course_status(request, language, speakers_language):
    """
    in this view the vaisc users can see specific status updates about a course
    that is currently under development
    """
    # Deleting any sessions regarding top-tier type of users
    # session.pop("programmer_username", None)  <-- these are flask change it
    # session.pop("programmer_logged_in", None) <-- these are flask change it
    # admin user session pop
    # admin user session pop

    # ACCESS CONTROL
    delete_teacher_user_session(request)

    # Get the current users
    current_basic_user = get_current_user(request, User, ObjectDoesNotExist)

    current_basic_user_profile = get_current_user_profile(
        request,
        User,
        BasicUserProfile,
        ObjectDoesNotExist
    )

    # Getting the current page course
    try:
        current_course = TeacherLanguageCourse.objects.get(
            course_language=language,
            course_speakers_language=speakers_language
        )
    except ObjectDoesNotExist:
        current_course = None

    # Getting all the course contributors
    try:
        current_course_contributors = TeacherUserProfile.objects.filter(
            course_language=language,
            course_speakers_language=speakers_language
        )
    except ObjectDoesNotExist:
        current_course_contributors = None

    # Getting all the course status
    try:
        current_course_status_updates = CourseStatusUpdate.objects.filter(
            course=current_course
        )
    except ObjectDoesNotExist:
        current_course_status_updates = None

    data = {
        "current_basic_user": current_basic_user,
        "current_basic_user_profile": current_basic_user_profile,
        "current_course": current_course,
        "current_course_contributors": current_course_contributors,
        "current_course_status_updates": current_course_status_updates,
    }

    if current_basic_user == None:
        return HttpResponseRedirect("/auth/login/")
    else:
        return render(request, "teacher_public_about/course_status.html", data)
