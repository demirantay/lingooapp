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
from basic_notifications.models import NotificationBase

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
    # At every page there will be 45 entries so always multiply it by that and
    # then reduce your objects
    current_page = page
    previous_page = page-1
    next_page = page+1

    feedback_records_starting_point = current_page * 46
    feedback_records_ending_point = feedback_records_starting_point + 46
    try:
        current_page_feedbacks = Feedback.objects.all().order_by(
            "-id"
        )[feedback_records_starting_point:feedback_records_ending_point]
    except ObjectDoesNotExist:
        current_page_feedbacks = None

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
        "current_page": current_page,
        "previous_page": previous_page,
        "next_page": next_page,
        "current_page_feedbacks": current_page_feedbacks,
    }

    if current_basic_user == None:
        return HttpResponseRedirect("/auth/login/")
    else:
        return render(request, "basic_feedback/landing_page.html", data)


def basic_feedback_read(request, feedback_id):
    """
    in this page the user can read a specific feedback, comment on it, or if
    it is the owners feedback it can delete or edit it
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

    # Current Feedback
    try:
        current_feedback = Feedback.objects.get(id=feedback_id)
    except ObjectDoesNotExist:
        current_feedback = None

    # Update the view of the feedback
    if current_feedback != None:
        current_feedback.views += 1
        current_feedback.save()

    # Getting the feedback dev answer
    try:
        current_feedback_dev_answers = FeedbackDevAnswer.objects.filter(
            feedback=current_feedback
        )
    except ObjectDoesNotExist:
        current_feedback_dev_answers = None

    # Getting Current Feedback Comments
    try:
        current_feedback_comments = FeedbackComment.objects.filter(
            feedback=current_feedback
        ).order_by("-karma")
    except ObjectDoesNotExist:
        current_feedback_comments = None

    # Getting Feedback Comment Replies
    try:
        current_feedback_comment_replies = FeedbackCommentReply.objects.filter(
            feedback=current_feedback
        )
    except ObjectDoesNotExist:
        current_feedback_comment_replies = None

    comment_replies = {}
    for reply in current_feedback_comment_replies:
        if reply.comment.id in comment_replies:
            comment_replies[reply.comment.id].append(reply)
        else:
            comment_replies[reply.comment.id] = []
            comment_replies[reply.comment.id].append(reply)

    comment_replies_amount = {}
    for comment in current_feedback_comments:
        reply_count = 0
        for reply in current_feedback_comment_replies:
            if reply.comment.id == comment.id:
                reply_count += 1
        comment_replies_amount[comment.id] = reply_count

    '''
    for i in current_feedback_comment_replies:
        amount = 0
        for j in current_feedback_comment_replies:
            if i.comment.id == j.comment.id:
                amount += 1
        comment_replies_amount[reply.comment.id] = amount
    '''

    # Create Comments form Processing
    empty_comment = False

    if request.POST.get("basic_feedback_comment_submit_btn"):
        content = request.POST.get("content")

        # check if it is empty
        if bool(content) == False or content == "":
            empty_comment = True
        else:
            new_comment = FeedbackComment(
                comment_owner=current_basic_user_profile,
                feedback=current_feedback,
                content=content
            )
            new_comment.save()
            # create neccessary notifications
            new_notification = NotificationBase(
                notification_owner=current_basic_user_profile,
                notified_user=current_feedback.user,
                status="feedback_comment",
                feedback_comment=new_comment,
            )
            new_notification.save()
            return HttpResponseRedirect(
                "/feedback/read/" + str(current_feedback.id) + "/"
            )

    # Comment Upvote form Processing
    if request.POST.get("basic_feedback_comment_upvote_btn"):
        hidden_comment_id = request.POST.get("hidden_comment_id")
        try:
            comment = FeedbackComment.objects.get(id=hidden_comment_id)
        except ObjectDoesNotExist:
            comment = None
        if comment != None:
            comment.karma += 1
            comment.save()
            return HttpResponseRedirect(
                "/feedback/read/" + str(current_feedback.id) + "/"
            )

    # Create Comment Reply Processing
    if request.POST.get("basic_feedback_comment_reply_submit_btn"):
        hidden_comment_id = request.POST.get("hidden_comment_id")
        reply_content = request.POST.get("reply_content")

        try:
            replied_comment = FeedbackComment.objects.get(id=hidden_comment_id)
        except ObjectDoesNotExist:
            replied_comment = None

        # check if the comment exists
        if reply_content != None:
            # check if the input is empty
            if bool(reply_content) == False or reply_content == "":
                pass
            else:
                # create a new comment reply
                new_reply = FeedbackCommentReply(
                    comment=replied_comment,
                    feedback=current_feedback,
                    reply_owner=current_basic_user_profile,
                    content=reply_content
                )
                new_reply.save()
                # create necessary notiications
                new_notification = NotificationBase(
                    notification_owner=current_basic_user_profile,
                    notified_user=replied_comment.comment_owner,
                    status="feedback_comment_reply",
                    feedback_comment_reply=new_reply,
                )
                new_notification.save()
                return HttpResponseRedirect(
                    "/feedback/read/" + str(current_feedback.id) + "/"
                )

    # Feedback Edit form procesing
    empty_update_input = False
    less_than_100_chars = False

    if request.POST.get("basic_feedback_update_submit_btn"):
        title = request.POST.get("update_title")
        content = request.POST.get("update_content")

        # check if the inputs are empty
        if bool(title) == False or title == "" or \
           bool(content) == False or content == "":
            empty_update_input = True
        else:
            # check if the length is less than 100 chars for content
            if len(content) < 100:
                less_than_100_chars = True
            else:
                # if everything is good create a new feedback
                current_feedback.title = title
                current_feedback.content = content
                current_feedback.save()
                return HttpResponseRedirect(
                    "/feedback/read/" + str(current_feedback.id) + "/"
                )

    # Feedback Delete form processing
    if request.POST.get("basic_feedback_delete_submit_btn"):
        # delete all the comment replies
        try:
            all_replies = FeedbackCommentReply.objects.filter(
                feedback=current_feedback
            )
        except ObjectDoesNotExist:
            all_replies = None

        if all_replies != None:
            all_replies.delete()

        # delete all the comments
        if current_feedback_comments != None:
            current_feedback_comments.delete()

        # delete the dev answers

        if current_feedback_dev_answers != None:
            current_feedback_dev_answers.delete()

        # delete the feedback
        if current_feedback != None:
            current_feedback.delete()

        return HttpResponseRedirect("/feedback/0/")

    data = {
        "current_basic_user": current_basic_user,
        "current_basic_user_profile": current_basic_user_profile,
        "current_teacher_profile": current_teacher_profile,
        "current_feedback": current_feedback,
        "comments_amount": len(current_feedback_comments),
        "current_feedback_dev_answers": current_feedback_dev_answers,
        "empty_comment": empty_comment,
        "current_feedback_comments": current_feedback_comments,
        "empty_update_input": empty_update_input,
        "less_than_100_chars": less_than_100_chars,
        "comment_replies": comment_replies,
        "comment_replies_amount": comment_replies_amount,
    }

    if current_basic_user == None:
        return HttpResponseRedirect("/auth/login/")
    else:
        return render(request, "basic_feedback/read.html", data)
