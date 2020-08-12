# Main Imports

# Django Imports
from django.shortcuts import render, get_object_or_404, HttpResponse
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.core.files import File
from django.contrib.auth.models import User

# My Module Imports


def profile_settings_edit_profile(request):
    """ a """
    data = {

    }
    return render(request, "profile_settings/edit_profile.html", data)


def profile_settings_change_password(request):
    """ a """
    data = {

    }
    return render(request, "profile_settings/change_password.html", data)


def profile_settings_email_sms(request):
    """ a """
    data = {

    }
    return render(request, "profile_settings/email_sms.html", data)
