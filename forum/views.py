# Main Imports

# Django Imports
from django.shortcuts import render, get_object_or_404, HttpResponse
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.core.files import File
from django.contrib.auth.models import User

# My Module Imports


def forum_landing_page(request):
    """ a """

    all_posts = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

    data = {
        "all_posts": all_posts,
    }
    return render(request, "forum/forum_landing_page.html", data)


def forum_create(request):
    """ a """

    data = {

    }
    return render(request, "forum/forum_create.html", data)


def forum_read(request, post_id):
    """ a """

    post_comments = [1, 1, 1, 1, 1, 1, 1, 1]

    data = {
        "post_comments": post_comments,
    }
    return render(request, "forum/forum_read.html", data)


def forum_update(request, post_id):
    """ a """

    data = {
    }
    return render(request, "forum/forum_update.html", data)
