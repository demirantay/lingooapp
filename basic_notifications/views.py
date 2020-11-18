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
from .models import NotificationBase, ForumPostCommentNotification
from .models import ForumCommentReplyNotification, CongressBillVoteNotification
from .models import FeedbackCommentNotification, FeedbackDevAnswerNotification
from .models import FeedbackCommentReplyNotification


def notifications(request, page):
    """
    in this page the user can see her notifications
    """
    # Deleting admin-typed user session
    # Deleting programmer-typed-user session
    # Deleting Teacher-typed user sessions

    data = {

    }

    return render(request, "basic_notifications/notifications.html", data)
