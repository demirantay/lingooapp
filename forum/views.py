# Main Imports

# Django Imports
from django.shortcuts import render, get_object_or_404, HttpResponse
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.core.files import File
from django.contrib.auth.models import User

# My Module Imports
from .models import ForumPost, ForumComment, ForumCommentReply
from profile_settings.models import BasicUserProfile
from teacher_authentication.models import TeacherUserProfile
from basic_language_explore.models import Language, Student
from basic_notifications.models import NotificationBase

from utils.session_utils import get_current_user, get_current_user_profile
from utils.session_utils import get_current_teacher_user_profile
from utils.access_control import delete_teacher_user_session
from algorithms.selection_sort import descending_selection_sort


def forum_landing_page(request, page):
    """
    This is the landing page of the forum feature of the site.
    """
    # Deleting any sessions regarding top-tier type of users
    # session.pop("programmer_username", None)  <-- these are flask change it
    # session.pop("programmer_logged_in", None) <-- these are flask change it
    # admin user session pop
    # admin user session pop

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

    # get all languages (categories)
    try:
        all_languages = Language.objects.all()
    except ObjectDoesNotExist:
        all_languages = None

    # Get pinned posts
    try:
        pinned_posts = ForumPost.objects.filter(is_pinned=True)
    except ObjectDoesNotExist:
        pinned_posts = None

    # get pinned post comments
    pinned_post_comments = {}
    for post in pinned_posts:
        comments = ForumComment.objects.filter(post=post)
        comment_count = 0
        for comment in comments:
            comment_count += 1
        pinned_post_comments[post.id] = comment_count

    # Get all of the posts
    # At every page there will be 45 entries so always multiply it by that and
    # then reduce your objects
    current_page = page
    previous_page = page-1
    next_page = page+1

    post_records_starting_point = current_page * 46
    post_records_ending_point = post_records_starting_point + 46
    try:
        current_page_posts = ForumPost.objects.all().order_by('-id')[post_records_starting_point:post_records_ending_point]
    except ObjectDoesNotExist:
        current_page_posts = None

    # getting posts comment count
    page_comments = {}
    for post in current_page_posts:
        comments = ForumComment.objects.filter(post=post)
        comment_count = 0
        for comment in comments:
            comment_count += 1
        page_comments[post.id] = comment_count

    # Post cell upvote form processing
    if request.POST.get("post_upvote_submit_btn"):
        hidden_post_id = request.POST.get("hidden_post_id")
        post = ForumPost.objects.get(id=hidden_post_id)
        # upvote the post
        post.karma += 1
        post.save()
        return HttpResponseRedirect("/forum/read/" + hidden_post_id + "/")

    # Post cell downvote form processing
    if request.POST.get("post_downvote_submit_btn"):
        hidden_post_id = request.POST.get("hidden_post_id")
        post = ForumPost.objects.get(id=hidden_post_id)
        # downvote the post
        post.karma -= 1
        post.save()
        return HttpResponseRedirect("/forum/read/" + hidden_post_id + "/")

    data = {
        "current_page_posts": current_page_posts,
        "page_comments": page_comments,
        "pinned_post_comments": pinned_post_comments,
        "current_page": page,
        "previous_page": previous_page,
        "next_page": next_page,
        "current_basic_user": current_basic_user,
        "current_basic_user_profile": current_basic_user_profile,
        "current_teacher_profile": current_teacher_profile,
        "all_languages": all_languages,
        "pinned_posts": pinned_posts,
    }

    if current_basic_user == None:
        return HttpResponseRedirect("/auth/login/")
    else:
        return render(request, "forum/forum_landing_page_v2.html", data)


def forum_category_page(request, category_language, page):
    """
    This is the landing page of the category pages
    """
    # Deleting any sessions regarding top-tier type of users
    # session.pop("programmer_username", None)  <-- these are flask change it
    # session.pop("programmer_logged_in", None) <-- these are flask change it
    # admin user session pop
    # admin user session pop

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

    # get all languages (categories)
    try:
        all_languages = Language.objects.all()
    except ObjectDoesNotExist:
        all_languages = None

    # current langauge:
    try:
        current_language = Language.objects.get(name=category_language)
    except ObjectDoesNotExist:
        current_language = None

    # if current language does not exist return 404
    if current_language == None:
        return HttpResponseRedirect("/404/")

    # Get pinned posts
    try:
        pinned_posts = ForumPost.objects.filter(is_pinned=True)
    except ObjectDoesNotExist:
        pinned_posts = None

    # Get pinned posts comments
    pinned_post_comments = {}
    for post in pinned_posts:
        comments = ForumComment.objects.filter(post=post)
        comment_count = 0
        for comment in comments:
            comment_count += 1
        pinned_post_comments[post.id] = comment_count

    # Get category posts
    # At every page there will be 45 entries so always multiply it by that and
    # then reduce your objects
    current_page = page
    previous_page = page-1
    next_page = page+1

    post_records_starting_point = current_page * 46
    post_records_ending_point = post_records_starting_point + 46
    try:
        current_page_posts = ForumPost.objects.filter(language=current_language).order_by('-id')[post_records_starting_point:post_records_ending_point]
    except ObjectDoesNotExist:
        current_page_posts = None

    # getting posts comment count
    page_comments = {}
    for post in current_page_posts:
        comments = ForumComment.objects.filter(post=post)
        comment_count = 0
        for comment in comments:
            comment_count += 1
        page_comments[post.id] = comment_count

    # Post cell upvote form processing
    if request.POST.get("post_upvote_submit_btn"):
        hidden_post_id = request.POST.get("hidden_post_id")
        post = ForumPost.objects.get(id=hidden_post_id)
        # upvote the post
        post.karma += 1
        post.save()

    # Post cell downvote form processing
    if request.POST.get("post_downvote_submit_btn"):
        hidden_post_id = request.POST.get("hidden_post_id")
        post = ForumPost.objects.get(id=hidden_post_id)
        # downvote the post
        post.karma -= 1
        post.save()

    data = {
        "current_basic_user": current_basic_user,
        "current_basic_user_profile": current_basic_user_profile,
        "current_teacher_profile": current_teacher_profile,
        "all_languages": all_languages,
        "current_language": current_language,
        "current_page": page,
        "previous_page": previous_page,
        "next_page": next_page,
        "current_page_posts": current_page_posts,
        "page_comments": page_comments,
        "pinned_posts": pinned_posts,
        "pinned_post_comments": pinned_post_comments,
    }

    if current_basic_user == None:
        return HttpResponseRedirect("/auth/login/")
    else:
        return render(request, "forum/forum_category_v2.html", data)


def forum_create(request):
    """
    in this view the users can create a forum post
    """
    # Deleting any sessions regarding top-tier type of users
    # session.pop("programmer_username", None)  <-- these are flask change it
    # session.pop("programmer_logged_in", None) <-- these are flask change it
    # admin user session pop
    # admin user session pop

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

    # get all languages (categories)
    try:
        all_languages = Language.objects.all()
    except ObjectDoesNotExist:
        all_languages = None

    # forum create post form processing
    empty_input = False

    if request.POST.get("forum_create_post_btn"):
        post_title = request.POST.get("post_title")
        post_language = request.POST.get("post_language")
        post_content = request.POST.get("post_content")

        # check if any of the inputs are empty
        if bool(post_title) == False or post_title == "" \
           or bool(post_content) == False or post_content == "":
            empty_input = True
        else:
            # get the language instance
            language_instance = Language.objects.get(name=post_language)
            # create the post
            new_post = ForumPost(
                user_profile=current_basic_user_profile,
                language=language_instance,
                post_title=post_title,
                content=post_content
            )
            new_post.save()
            return HttpResponseRedirect("/forum/read/" + str(new_post.id) + "/")

    data = {
        "current_basic_user": current_basic_user,
        "current_basic_user_profile": current_basic_user_profile,
        "current_teacher_profile": current_teacher_profile,
        "all_languages": all_languages,
        "empty_input": empty_input,
    }

    if current_basic_user == None:
        return HttpResponseRedirect("/auth/login/")
    else:
        return render(request, "forum/forum_create.html", data)


def forum_read(request, post_id):
    """
    in this page the users can read a single post in the forum feature
    """
    # Deleting any sessions regarding top-tier type of users
    # session.pop("programmer_username", None)  <-- these are flask change it
    # session.pop("programmer_logged_in", None) <-- these are flask change it
    # admin user session pop
    # admin user session pop

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

    # get all languages (categories)
    try:
        all_languages = Language.objects.all()
    except ObjectDoesNotExist:
        all_languages = None

    # get the current post
    try:
        current_post = ForumPost.objects.get(id=post_id)
    except ObjectDoesNotExist:
        current_post = None

    # if the post id is not existing redirect to 404
    if current_post == None:
        return HttpResponseRedirect("/404/")

    # Update the current post view count
    current_post.views += 1
    current_post.save()

    # check if the post is owned by the current user if it is pass it on to
    # the template logic
    current_user_is_owner = False
    if current_post.user_profile == current_basic_user_profile:
        current_user_is_owner = True

    # current post upvote form processing
    if request.POST.get("post_content_upvote"):
        current_post.karma += 1
        current_post.save()

    # current post downvote form processing
    if request.POST.get("post_content_downvote"):
        current_post.karma -= 1
        current_post.save()

    # get current post owners all student profiles
    try:
        post_owner_student_profiles = Student.objects.filter(
            basic_user_profile=current_post.user_profile
        ).order_by("xp")
    except ObjectDoesNotExist:
        post_owner_student_profiles = None

    # get all the coments
    try:
        current_post_comments = ForumComment.objects.filter(post=current_post)
        # descending sorted array by the comment's karma points
        # used algoritmg: insertion sort
        current_post_comments_sorted = []
        for comment in current_post_comments:
            current_post_comments_sorted.append(comment)

        for i in range(len(current_post_comments_sorted)):
            for j in range(len(current_post_comments_sorted)):
                if current_post_comments_sorted[i].karma > current_post_comments_sorted[j].karma:
                    # swap
                    temporary = current_post_comments_sorted[i]
                    current_post_comments_sorted[i] = current_post_comments_sorted[j]
                    current_post_comments_sorted[j] = temporary
                else:
                    continue
    except ObjectDoesNotExist:
        current_post_comments = None
        current_post_comments_sorted = None

    # Get all of the flags of each comment owner
    comment_student_profiles = {}
    for comment in current_post_comments:
        if comment.user_profile.id in comment_student_profiles:
            pass
        else:
            student_profiles = Student.objects.filter(
                basic_user_profile=comment.user_profile
            ).order_by("xp")
            comment_student_profiles[comment.user_profile.id] = student_profiles

    # comment create form processing
    if request.POST.get("comment_submit_btn"):
        comment_content = request.POST.get("comment_content")
        new_comment = ForumComment(
            user_profile=current_basic_user_profile,
            post=current_post,
            content=comment_content
        )
        new_comment.save()
        # update and create notificiations
        new_notification = NotificationBase(
            notification_owner=current_basic_user_profile,
            notified_user=current_post.user_profile,
            status="forum_post_comment",
            forum_post_comment=new_comment,
        )
        new_notification.save()
        return HttpResponseRedirect("/forum/read/"+str(current_post.id)+"/")

    # comment upote form processing
    if request.POST.get("comment_upvote_submit_btn"):
        hidden_comment_id = request.POST.get("hidden_comment_id")
        current_comment = ForumComment.objects.get(id=hidden_comment_id)
        current_comment.karma += 1
        current_comment.save()

    # comment downvote form processing
    if request.POST.get("comment_downvote_submit_btn"):
        hidden_comment_id = request.POST.get("hidden_comment_id")
        current_comment = ForumComment.objects.get(id=hidden_comment_id)
        current_comment.karma -= 1
        current_comment.save()

    # Delete the post and its comments form processing
    if request.POST.get("delete_submit_btn"):
        # check if the current user is the owner of the post
        if current_post.user_profile == current_basic_user_profile:
            # delete the ppost
            current_post.delete()
            # delete all the comments
            current_post_comments.delete()
            current_post_comments_sorted = []
            # redirect to landing page
            return HttpResponseRedirect("/forum/0/")

    # Get the current post's comments replies
    try:
        current_post_comment_replies = ForumCommentReply.objects.filter(
            forum_post=current_post
        )
    except ObjectDoesNotExist:
        current_post_comment_replies = None

    comment_replies = {}
    for reply in current_post_comment_replies:
        if reply.comment.id in comment_replies:
            comment_replies[reply.comment.id].append(reply)
        else:
            comment_replies[reply.comment.id] = []
            comment_replies[reply.comment.id].append(reply)

    comment_replies_amount = {}
    for comment in current_post_comments:
        reply_count = 0
        for reply in current_post_comment_replies:
            if reply.comment.id == comment.id:
                reply_count += 1
        comment_replies_amount[comment.id] = reply_count

    # Comment Reply Form Processing
    if request.POST.get("forum_read_comment_reply_submit_btn"):
        hidden_comment_id = request.POST.get("hidden_comment_id")
        comment_reply_content = request.POST.get("comment_reply_content")

        # get the current comment
        try:
            current_comment = ForumComment.objects.get(id=hidden_comment_id)
        except ObjectDoesNotExist:
            current_comment = None

        # create new reply if the inputs arent empty
        if bool(comment_reply_content) == False or comment_reply_content == "":
            pass
        else:
            new_comment_reply = ForumCommentReply(
                comment=current_comment,
                forum_post=current_post,
                reply_owner=current_basic_user_profile,
                content=comment_reply_content,
            )
            new_comment_reply.save()
            # create the neccessary notifications
            new_notification = NotificationBase(
                notification_owner=current_basic_user_profile,
                notified_user=current_comment.user_profile,
                status="forum_comment_reply",
                forum_comment_reply=new_comment_reply,
            )
            new_notification.save()
            return HttpResponseRedirect(
                "/forum/read/" + str(current_post.id) + "/"
            )

    # Comment Reply Upvote Form processing
    if request.POST.get("forum_read_comment_reply_upvote_submit_btn"):
        hidden_reply_id = request.POST.get("hidden_reply_id")
        # get current reply
        try:
            current_reply = ForumCommentReply.objects.get(id=hidden_reply_id)
        except ObjectDoesNotExist:
            current_reply = None
        current_reply.karma += 1
        current_reply.save()
        return HttpResponseRedirect(
            "/forum/read/" + str(current_post.id) + "/"
        )

    # Comment Reply Downvote Form Processing
    if request.POST.get("forum_read_comment_reply_downvote_submit_btn"):
        hidden_reply_id = request.POST.get("hidden_reply_id")
        # get current reply
        try:
            current_reply = ForumCommentReply.objects.get(id=hidden_reply_id)
        except ObjectDoesNotExist:
            current_reply = None
        current_reply.karma -= 1
        current_reply.save()
        return HttpResponseRedirect(
            "/forum/read/" + str(current_post.id) + "/"
        )

    # Forum Read Delete form Processing
    if request.POST.get("basic_forum_read_delete_submit_btn"):
        # check if the post is the owned by the current user
        if current_post.user_profile == current_basic_user_profile:
            # delete all the comment replies
            try:
                all_replies = ForumCommentReply.objects.filter(
                    forum_post=current_post
                )
            except ObjectDoesNotExist:
                all_replies = None

            if all_replies != None:
                all_replies.delete()

            # delete all the comments
            if current_post_comments != None:
                current_post_comments.delete()

            # delete the feedback
            if current_post != None:
                current_post.delete()

            return HttpResponseRedirect("/forum/0/")
        else:
            pass

    data = {
        "current_basic_user": current_basic_user,
        "current_basic_user_profile": current_basic_user_profile,
        "current_teacher_profile": current_teacher_profile,
        "all_languages": all_languages,
        "current_post": current_post,
        "current_post_comments": current_post_comments,
        "current_post_comments_amount": len(current_post_comments),
        "current_post_comments_sorted": current_post_comments_sorted,
        "current_user_is_owner": current_user_is_owner,
        "post_owner_student_profiles": post_owner_student_profiles,
        "post_owner_highest_xp_profile": post_owner_student_profiles[0],
        "comment_replies": comment_replies,
        "comment_replies_amount": comment_replies_amount,
        "comment_student_profiles": comment_student_profiles,
    }

    if current_basic_user == None:
        return HttpResponseRedirect("/auth/login/")
    else:
        return render(request, "forum/forum_read_v2.html", data)


def forum_update(request, post_id):
    """
    in this view the users update their own forum post
    """
    # Deleting any sessions regarding top-tier type of users
    # session.pop("programmer_username", None)  <-- these are flask change it
    # session.pop("programmer_logged_in", None) <-- these are flask change it
    # admin user session pop
    # admin user session pop

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

    # get all languages (categories)
    try:
        all_languages = Language.objects.all()
    except ObjectDoesNotExist:
        all_languages = None

    # check if the post is current users's post. If it is not redirect
    # the users should not be able to edit somebody else's post
    try:
        current_post = ForumPost.objects.get(id=post_id)
    except ObjectDoesNotExist:
        current_post = None

    if current_post == None:
        return HttpResponseRedirect("/404/")
    elif current_post.user_profile != current_basic_user_profile:
        return HttpResponseRedirect("/404/")

    # Post Update form processing
    empty_input = False

    if request.POST.get("update_post_submit_btn"):
        post_title = request.POST.get("post_title")
        post_content = request.POST.get("post_content")

        # check if any of the inputs are empty
        if bool(post_title) == False or post_title == "" \
           or bool(post_content) == False or post_content == "":
            empty_input = True
        else:
            # update the post and redirect
            current_post.post_title = post_title
            current_post.content = post_content
            current_post.save()
            return HttpResponseRedirect("/forum/read/"+str(current_post.id)+"/")

    data = {
        "current_basic_user": current_basic_user,
        "current_basic_user_profile": current_basic_user_profile,
        "current_teacher_profile": current_teacher_profile,
        "all_languages": all_languages,
        "current_post": current_post,
        "empty_input": empty_input,
    }

    if current_basic_user == None:
        return HttpResponseRedirect("/auth/login/")
    else:
        return render(request, "forum/forum_update.html", data)
