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


def teacher_reading_build(request, course_language, course_speaker_language):
    """
    in this page the teacher can build the neccessary reading lessons
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

    # Adding a new lesson to the teacher course
    empty_lesson_name = False

    if request.POST.get("teacher_reading_builder_lesson_add_button"):
        lesson_name = request.POST.get("lesson_name")
        lesson_level = request.POST.get("lesson_level")

        if bool(lesson_name) == False or lesson_name == "":
            empty_lesson_name = True
        else:
            print(lesson_name, lesson_level)

    # Getting all of the lessons of the current course

    # Automation for the teacher course

    data = {
        "current_basic_user": current_basic_user,
        "current_basic_user_profile": current_basic_user_profile,
        "current_teacher_profile": current_teacher_profile,
        "empty_lesson_name": empty_lesson_name,
    }

    if "teacher_user_logged_in" in request.session:
        return render(request, "teacher_reading_builder/build.html", data)
    else:
        return HttpResponseRedirect("/")


def teacher_reading_update(request, id):
    """

    """

    data = {

    }

    return render(request, "teacher_reading_builder/update.html", data)


def teacher_reading_add_sentence(request):
    """

    """

    data = {

    }

    return render(request, "teacher_reading_builder/add_sentence.html", data)
