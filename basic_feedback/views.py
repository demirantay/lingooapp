# Main Imports
import json

# Django Imports
from django.shortcuts import render, get_object_or_404, HttpResponse
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.core.files import File
from django.contrib.auth.models import User

# My Module ImportsImports
from .models import Feedback, FeedbackDevAnswer, FeedbackComment
from .models import FeedbackCommentReply
from profile_settings.models import BasicUserProfile
from teacher_authentication.models import TeacherUserProfile
from utils.session_utils import get_current_user, get_current_user_profile
from utils.session_utils import get_current_teacher_user_profile
from utils.access_control import delete_teacher_user_session


def basic_feedback_landing_page(request, page):
    """
    In this view the users can see all of the feedbacks and their answers.
    and also the users can create feedbacks in this view
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

    # All of the feedbacks

    # Feed back create form processing
    empty_input = False
    less_than_100_chars = False

    if request.POST.get("basic_feedback_create_submit_btn"):
        title = request.POST.get("feedback_title")
        content = request.POST.get("feedback_content")

        # check if the inputs are empty
        if bool(title) == False or title == "" or \
           bool(content) == False or content == "":
            empty_input = True
        else:
            # check if the length is less than 100 chars for content
            if len(content) < 100:
                less_than_100_chars = True
            else:
                # if everything is good create a new feedback
                new_feedback = Feedback(
                    user=current_basic_user_profile,
                    title=title,
                    content=content
                )
                new_feedback.save()
                return HttpResponseRedirect(
                    "/feedback/read/" + str(new_feedback.id) + "/"
                )

    data = {
        "current_basic_user": current_basic_user,
        "current_basic_user_profile": current_basic_user_profile,
        "current_teacher_profile": current_teacher_profile,
        "empty_input": empty_input,
        "less_than_100_chars": less_than_100_chars,
    }

    if current_basic_user == None:
        return HttpResponseRedirect("/auth/login/")
    else:
        return render(request, "basic_feedback/landing_page.html", data)


def basic_feedback_read(request, feedback_id):
    """

    """

    data = {

    }

    return render(request, "basic_feedback/read.html", data)
