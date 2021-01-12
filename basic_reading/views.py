# Main Imports

# Django Imports
from django.shortcuts import render, get_object_or_404, HttpResponse
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

# My Module Imports


def basic_reading_learn_start(request):
    """

    """

    data = {

    }

    return render(request, "basic_reading/start.html", data)


def basic_reading_learn(request):
    """

    """

    data = {

    }

    return render(request, "basic_reading/learn.html", data)
