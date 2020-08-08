# Main Imports

# Django Imports
from django.shortcuts import render, get_object_or_404, HttpResponse
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.core.files import File
from django.contrib.auth.models import User

# My Module Imports


def about(request):
    """about page explains the company's vision and mission"""

    data = {}
    return render(request, "about/about.html", data)


def about_community_rules(request):
    """asd"""

    data = {}
    return render(request, "about/community_rules.html", data)


def about_terms(request):
    """asd"""

    data = {}
    return render(request, "about/terms_and_agreements.html", data)


def about_privacy(request):
    """asd"""

    data = {}
    return render(request, "about/privacy_policy.html", data)
