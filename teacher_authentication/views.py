# Main Imports

# Django Imports
from django.shortcuts import render, get_object_or_404, HttpResponse
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.core.files import File
from django.contrib.auth.models import User

# My Module Imports
from .models import TeacherApplication, TeacherUserProfile
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
    above_13_years_old = True
    languages_are_same = False

    if request.POST.get("course_apply_submit_btn"):
        course_language = request.POST.get("course_language")
        speakers_language = request.POST.get("speakers_language")
        native_language = request.POST.get("native_language")
        course_language_text = request.POST.get("course_language_text")
        speakers_language_text = request.POST.get("speakers_language_text")
        email = request.POST.get("email")
        above_13_years_old = request.POST.get("above_13_years_old")

        # Teacher User Create Algorithm:
        # ------------------------------
        # 1 - user applies for the teacher position
        # 2 - An application record is created
        # 3 - An teacher profile is created NO django user is created atm
        #     it will be created once the user is signing up
        # 4 - The application awaits admin permission for signup.
        # 5 - signup creates a new django user and connects it to the already
        #     created teacher profile. And the profile gets updated with new
        #     signup data.

        # check if both languages are same
        if course_language == speakers_language:
            languages_are_same = True
        else:
            # check if above 13 years old
            if above_13_years_old == None:
                above_13_years_old = False
            else:
                # check if any input is empty
                if bool(native_language) == False\
                   or native_language == ""\
                   or bool(course_language_text) == False \
                   or course_language_text == ""\
                   or bool(speakers_language_text) == False\
                   or speakers_language_text == ""\
                   or bool(email) == False\
                   or email == "":
                    empty_credentials = True
                else:
                    # create application record and
                    # redirect to a thank you page
                    new_application = TeacherApplication(
                        course_language=course_language,
                        course_speakers_language=speakers_language,
                        native_language=native_language,
                        course_language_why_are_you_interested_text=course_language_text,
                        speakers_language_why_are_you_interested_text=speakers_language_text,
                        email=email,
                        older_than_13=True
                    )
                    new_application.save()
                    # A new teacher profile is created
                    new_teacher_profile = TeacherUserProfile(
                        native_language=native_language,
                        course_language=course_language,
                        course_speakers_language=speakers_language,
                        email=email,
                    )
                    new_teacher_profile.save()
                    return HttpResponseRedirect("/contrib/apply/thanks/")

    data = {
        "current_basic_user": current_basic_user,
        "current_basic_user_profile": current_basic_user_profile,
        "languages_are_same": languages_are_same,
        "above_13_years_old": above_13_years_old,
        "empty_credentials": empty_credentials,
    }

    if current_basic_user == None:
        return HttpResponseRedirect("/auth/login/")
    else:
        return render(request, "teacher_authentication/apply.html", data)


def application_thank_you_page(request):
    """
    Users get redirected to this page if they apply to the teacher program.
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

    data = {
        "current_basic_user": current_basic_user,
        "current_basic_user_profile": current_basic_user_profile,
    }

    if current_basic_user == None:
        return HttpResponseRedirect("/auth/login/")
    else:
        return render(request, "teacher_authentication/thank_you.html", data)


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
