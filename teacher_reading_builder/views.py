# Main Imports

# Django Imports
from django.shortcuts import render, get_object_or_404, HttpResponse
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

# My Module Imports


def teacher_reading_build(request):
    """

    """

    data = {

    }

    return render(request, "teacher_reading_builder/build.html", data)


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
