# Main Imports

# Django Imports
from django.shortcuts import render, get_object_or_404, HttpResponse
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.core.files import File
from django.contrib.auth.models import User

# My Module Imports
from .models import ContactUsMessage
from profile_settings.models import BasicUserProfile
from utils.session_utils import get_current_user, get_current_user_profile
from utils.access_control import delete_teacher_user_session


def about(request):
    """
    about page explains the company's vision and mission
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

    data = {
        "current_basic_user": current_basic_user,
        "current_basic_user_profile": current_basic_user_profile,
    }
    return render(request, "about/about.html", data)


def contact_us(request):
    """
    contact us page for the anonumouys users
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

    # Contact Us Form Processing
    empty_input = False
    submitted_message = False

    if request.POST.get("about-contact-us-form-submit-btn"):
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        # check if they are empty
        if bool(name) == False or name == "" or \
           bool(email) == False or email == "" or \
           bool(message) == False or message == "":
            empty_input = True
        else:
            # submit the message
            new_message = ContactUsMessage(
                name=name, email=email, message=message
            )
            new_message.save()
            submitted_message = True

    data = {
        "current_basic_user": current_basic_user,
        "current_basic_user_profile": current_basic_user_profile,
        "empty_input": empty_input,
        "submitted_message": submitted_message,
    }
    return render(request, "about/contact.html", data)


def about_community_rules(request):
    """community rules page explains the platforms community rules"""
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

    data = {
        "current_basic_user": current_basic_user,
        "current_basic_user_profile": current_basic_user_profile,
    }
    return render(request, "about/community_rules.html", data)


def about_terms(request):
    """terms and agreements epxlains the terms of the platform """
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

    data = {
        "current_basic_user": current_basic_user,
        "current_basic_user_profile": current_basic_user_profile,
    }
    return render(request, "about/terms_and_agreements.html", data)


def about_privacy(request):
    """this view explains the privacy policy of the platform"""
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

    data = {
        "current_basic_user": current_basic_user,
        "current_basic_user_profile": current_basic_user_profile,
    }
    return render(request, "about/privacy_policy.html", data)
