# Main Imports
import json

# Django Imports
from django.shortcuts import render, get_object_or_404, HttpResponse
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.core.files import File
from django.contrib.auth.models import User
from django.utils import timezone

# My Module ImportsImports
from .models import NotificationBase
from profile_settings.models import BasicUserProfile
from teacher_authentication.models import TeacherUserProfile
from utils.session_utils import get_current_user, get_current_user_profile
from utils.session_utils import get_current_teacher_user_profile
from utils.access_control import delete_teacher_user_session


def notifications(request, page):
    """
    in this page the user can see her notifications
    """
    # Deleting admin-typed user session
    # Deleting programmer-typed-user session
    # Deleting Teacher-typed user sessions

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

    # Getting the current teacher profile
    current_teacher_profile = get_current_teacher_user_profile(
        request,
        User,
        TeacherUserProfile,
        ObjectDoesNotExist
    )

    # Get all of the notifications
    try:
        all_notifications = NotificationBase.objects.filter(
            notified_user=current_basic_user_profile
        ).order_by("-id")
    except ObjectDoesNotExist:
        all_notifications = None

    # check if the user has unread notifications
    has_unread_notifications = False

    for notification in all_notifications:
        if notification.is_read == False:
            has_unread_notifications = True
            break
        else:
            continue

    # Since the page is visited make all of the notiications read = True

    data = {
        "current_basic_user": current_basic_user,
        "current_basic_user_profile": current_basic_user_profile,
        "current_teacher_profile": current_teacher_profile,
        "all_notifications": all_notifications,
        "has_unread_notifications": has_unread_notifications,
    }

    if current_basic_user == None:
        return HttpResponseRedirect("/auth/login/")
    else:
        return render(request, "basic_notifications/notifications.html", data)
