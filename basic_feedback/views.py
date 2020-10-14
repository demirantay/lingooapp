# Main Imports
import json

# Django Imports
from django.shortcuts import render, get_object_or_404, HttpResponse
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.core.files import File
from django.contrib.auth.models import User

# My Module ImportsImports


def basic_feedback_landing_page(request):
    """

    """

    data = {

    }

    return render(request, "basic_feedback/landing_page.html", data)


def basic_feedback_read(request, feedback_id):
    """

    """

    data = {

    }

    return render(request, "basic_feedback/read.html", data)
