# Main Imports

# Django Imports
from django.shortcuts import render, get_object_or_404, HttpResponse
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.core.files import File
from django.contrib.auth.models import User

# My Module Imports
from .models import ForumPost, ForumComment
from profile_settings.models import BasicUserProfile
from basic_language_explore.models import Language
from utils.session_utils import get_current_user, get_current_user_profile
from algorithms.selection_sort import descending_selection_sort


def forum_landing_page(request):
    """
    This is the landing page of the forum feature of the site.
    """
    # Deleting any sessions regarding top-tier type of users
    # session.pop("programmer_username", None)  <-- these are flask change it
    # session.pop("programmer_logged_in", None) <-- these are flask change it
    # admin user session pop
    # admin user session pop

    # Get the current users
    current_basic_user = get_current_user(request, User, ObjectDoesNotExist)

    current_basic_user_profile = get_current_user_profile(
        request,
        User,
        BasicUserProfile,
        ObjectDoesNotExist
    )

    # get all languages (categories)
    try:
        all_languages = Language.objects.all()
    except ObjectDoesNotExist:
        all_languages = None

    # get all posts

    all_posts = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

    data = {
        "all_posts": all_posts,
        "current_basic_user": current_basic_user,
        "current_basic_user_profile": current_basic_user_profile,
    }

    if current_basic_user == None:
        return HttpResponseRedirect("/auth/login/")
    else:
        return render(request, "forum/forum_landing_page.html", data)


def forum_category_page(request, category_language):
    """
    This is the landing page of the category pages
    """
    # Deleting any sessions regarding top-tier type of users
    # session.pop("programmer_username", None)  <-- these are flask change it
    # session.pop("programmer_logged_in", None) <-- these are flask change it
    # admin user session pop
    # admin user session pop

    # Get the current users
    current_basic_user = get_current_user(request, User, ObjectDoesNotExist)

    current_basic_user_profile = get_current_user_profile(
        request,
        User,
        BasicUserProfile,
        ObjectDoesNotExist
    )

    all_posts = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

    data = {
        "all_posts": all_posts,
        "current_basic_user": current_basic_user,
        "current_basic_user_profile": current_basic_user_profile,
    }

    if current_basic_user == None:
        return HttpResponseRedirect("/auth/login/")
    else:
        return render(request, "forum/forum_category_page.html", data)


def forum_create(request):
    """
    in this view the users can create a forum post
    """
    # Deleting any sessions regarding top-tier type of users
    # session.pop("programmer_username", None)  <-- these are flask change it
    # session.pop("programmer_logged_in", None) <-- these are flask change it
    # admin user session pop
    # admin user session pop

    # Get the current users
    current_basic_user = get_current_user(request, User, ObjectDoesNotExist)

    current_basic_user_profile = get_current_user_profile(
        request,
        User,
        BasicUserProfile,
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
            return HttpResponseRedirect("/forum/" + str(new_post.id) + "/")

    data = {
        "current_basic_user": current_basic_user,
        "current_basic_user_profile": current_basic_user_profile,
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

    # Get the current users
    current_basic_user = get_current_user(request, User, ObjectDoesNotExist)

    current_basic_user_profile = get_current_user_profile(
        request,
        User,
        BasicUserProfile,
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

    # comment create form processing
    if request.POST.get("comment_submit_btn"):
        comment_content = request.POST.get("comment_content")
        new_comment = ForumComment(
            user_profile=current_basic_user_profile,
            post=current_post,
            content=comment_content
        )
        new_comment.save()
        return HttpResponseRedirect("/forum/"+str(current_post.id)+"/")

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

    data = {
        "current_basic_user": current_basic_user,
        "current_basic_user_profile": current_basic_user_profile,
        "all_languages": all_languages,
        "current_post": current_post,
        "current_post_comments": current_post_comments,
        "current_post_comments_sorted": current_post_comments_sorted,
        "current_user_is_owner": current_user_is_owner,
    }

    if current_basic_user == None:
        return HttpResponseRedirect("/auth/login/")
    else:
        return render(request, "forum/forum_read.html", data)


def forum_update(request, post_id):
    """
    in this view the users update their own forum post
    """
    # Deleting any sessions regarding top-tier type of users
    # session.pop("programmer_username", None)  <-- these are flask change it
    # session.pop("programmer_logged_in", None) <-- these are flask change it
    # admin user session pop
    # admin user session pop

    # Get the current users
    current_basic_user = get_current_user(request, User, ObjectDoesNotExist)

    current_basic_user_profile = get_current_user_profile(
        request,
        User,
        BasicUserProfile,
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
        post_language = request.POST.get("post_language")
        post_content = request.POST.get("post_content")

        # check if any of the inputs are empty
        if bool(post_title) == False or post_title == "" \
           or bool(post_content) == False or post_content == "":
            empty_input = True
        else:
            # get the language instance
            language_instance = Language.objects.get(name=post_language)
            # update the post and redirect
            current_post.post_title = post_title
            current_post.language = language_instance
            current_post.content = post_content
            current_post.save()
            return HttpResponseRedirect("/forum/"+str(current_post.id)+"/")

    data = {
        "current_basic_user": current_basic_user,
        "current_basic_user_profile": current_basic_user_profile,
        "all_languages": all_languages,
        "current_post": current_post,
        "empty_input": empty_input,
    }

    if current_basic_user == None:
        return HttpResponseRedirect("/auth/login/")
    else:
        return render(request, "forum/forum_update.html", data)
