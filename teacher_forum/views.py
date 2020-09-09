# Main Imports

# Django Imports
from django.shortcuts import render, get_object_or_404, HttpResponse
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.core.files import File
from django.contrib.auth.models import User

# My Module Imports
from .models import TeacherForumPost, TeacherForumComment
from profile_settings.models import BasicUserProfile
from teacher_authentication.models import TeacherUserProfile
from utils.session_utils import get_current_user, get_current_user_profile
from utils.session_utils import get_current_teacher_user_profile


def teacher_forum_landing_page(request, page):
    """
    in this page teacher can see all of the forum posts
    """
    # Deleting admin-typed user session
    # Deleting programmer-typed-user session

    # Get the current users
    current_basic_user = get_current_user(request, User, ObjectDoesNotExist)

    current_basic_user_profile = get_current_user_profile(
        request,
        User,
        BasicUserProfile,
        ObjectDoesNotExist
    )

    # Getting the teacher profile
    current_teacher_profile = get_current_teacher_user_profile(
        request,
        User,
        TeacherUserProfile,
        ObjectDoesNotExist
    )

    # getting the page posts
    # At every page there will be 45 entries so always multiply it by that and
    # then reduce your objects
    current_page = page
    previous_page = page-1
    next_page = page+1

    post_records_starting_point = current_page * 46
    post_records_ending_point = post_records_starting_point + 46

    try:
        current_page_posts = TeacherForumPost.objects.all().order_by("-id")[post_records_starting_point:post_records_ending_point]
    except ObjectDoesNotExist:
        current_page_posts = None

    # getting posts comment count
    page_comments = {}
    for post in current_page_posts:
        comments = TeacherForumComment.objects.filter(post=post)
        comment_count = 0
        for comment in comments:
            comment_count += 1
        page_comments[post.id] = comment_count

    # post upvote form processing
    if request.POST.get("teacher_forum_landing_upvote_submit"):
        hidden_post_id = request.POST.get("hidden_post_id")
        post = TeacherForumPost.objects.get(id=hidden_post_id)
        # upvote the post
        post.karma += 1
        post.save()
        return HttpResponseRedirect("/teacher/forum/read/"+str(post.id)+"/")

    data = {
        "current_basic_user": current_basic_user,
        "current_basic_user_profile": current_basic_user_profile,
        "current_teacher_profile": current_teacher_profile,
        "current_page_posts": current_page_posts,
        "current_page": current_page,
        "previous_page": previous_page,
        "next_page": next_page,
        "current_page_posts": current_page_posts,
        "page_comments": page_comments,
    }

    if "teacher_user_logged_in" in request.session:
        return render(request, "teacher_forum/landing_page.html", data)
    else:
        return HttpResponseRedirect("/")


def teacher_forum_create(request):
    """
    in this view the teacher can create a forum post
    """
    # Deleting admin-typed user session
    # Deleting programmer-typed-user session

    # Get the current users
    current_basic_user = get_current_user(request, User, ObjectDoesNotExist)

    current_basic_user_profile = get_current_user_profile(
        request,
        User,
        BasicUserProfile,
        ObjectDoesNotExist
    )

    # Getting the teacher profile
    current_teacher_profile = get_current_teacher_user_profile(
        request,
        User,
        TeacherUserProfile,
        ObjectDoesNotExist
    )

    # forum create post form processing
    empty_input = False

    if request.POST.get("teacher_forum_create_post_btn"):
        post_title = request.POST.get("post_title")
        post_content = request.POST.get("post_content")

        # check if any of the inputs are empty
        if bool(post_title) == False or post_title == "" \
           or bool(post_content) == False or post_content == "":
            empty_input = True
        else:
            new_post = TeacherForumPost(
                teacher=current_teacher_profile,
                course=current_teacher_profile.teacher_course,
                post_title=post_title,
                content=post_content
            )
            new_post.save()
            return HttpResponseRedirect(
                "/teacher/forum/read/"+str(new_post.id)+"/"
            )

    data = {
        "current_basic_user": current_basic_user,
        "current_basic_user_profile": current_basic_user_profile,
        "current_teacher_profile": current_teacher_profile,
        "empty_input": empty_input,
    }

    if "teacher_user_logged_in" in request.session:
        return render(request, "teacher_forum/create.html", data)
    else:
        return HttpResponseRedirect("/")


def teacher_forum_read(request, post_id):
    """
    in this view the teacher can view other or their own posts information and
    its content with comments
    """
    # Deleting admin-typed user session
    # Deleting programmer-typed-user session

    # Get the current users
    current_basic_user = get_current_user(request, User, ObjectDoesNotExist)

    current_basic_user_profile = get_current_user_profile(
        request,
        User,
        BasicUserProfile,
        ObjectDoesNotExist
    )

    # Getting the teacher profile
    current_teacher_profile = get_current_teacher_user_profile(
        request,
        User,
        TeacherUserProfile,
        ObjectDoesNotExist
    )

    # Get the current post
    try:
        current_post = TeacherForumPost.objects.get(id=post_id)
    except ObjectDoesNotExist:
        current_post = None

    # if the post id is not existing redirect to 404
    if current_post == None:
        return HttpResponseRedirect("/404/")

    # check if the post is owned by the current user if it is pass it on to
    # the template logic
    current_user_is_teacher = False
    if current_post.teacher == current_teacher_profile:
        current_user_is_teacher = True

    # current post upvote form processing
    if request.POST.get("teacher_forum_read_post_upvote_btn"):
        current_post.karma += 1
        current_post.save()

    # current post downvote form processing
    if request.POST.get("teacher_forum_read_post_downvote_btn"):
        current_post.karma -= 1
        current_post.save()

    # get all the coments
    try:
        all_post_comments = TeacherForumComment.objects.filter(
            post=current_post
        ).order_by("-id")
    except ObjectDoesNotExist:
        all_post_comments = None

    # comment upote form processing
    if request.POST.get("teacher_forum_comment_upvote_submit"):
        hidden_comment_id = request.POST.get("hidden_comment_id")
        current_comment = TeacherForumComment.objects.get(id=hidden_comment_id)
        current_comment.karma += 1
        current_comment.save()
        return HttpResponseRedirect(
            "/teacher/forum/read/"+str(current_post.id)+"/"
        )

    # comment downvote form processing
    if request.POST.get("teacher_forum_comment_downvote_submit"):
        hidden_comment_id = request.POST.get("hidden_comment_id")
        current_comment = TeacherForumComment.objects.get(id=hidden_comment_id)
        current_comment.karma -= 1
        current_comment.save()
        return HttpResponseRedirect(
            "/teacher/forum/read/"+str(current_post.id)+"/"
        )

    # comment create form processing
    if request.POST.get("teacher_forum_comment_subtmit_btn"):
        comment_content = request.POST.get("comment_content")
        # check if it is empty
        if bool(comment_content) == False or comment_content == "":
            pass
        else:
            new_comment = TeacherForumComment(
                teacher=current_teacher_profile,
                post=current_post,
                content=comment_content
            )
            new_comment.save()
            return HttpResponseRedirect(
                "/teacher/forum/read/"+str(current_post.id)+"/"
            )

    # Delete the post and its comments form processing


    data = {
        "current_basic_user": current_basic_user,
        "current_basic_user_profile": current_basic_user_profile,
        "current_teacher_profile": current_teacher_profile,
        "current_post": current_post,
        "current_user_is_teacher": current_user_is_teacher,
        "all_post_comments": all_post_comments,
    }

    if "teacher_user_logged_in" in request.session:
        return render(request, "teacher_forum/read.html", data)
    else:
        return HttpResponseRedirect("/")


def teacher_forum_update(request, post_id):
    """
    in this view the teacher can update their own posts
    """


    # check if the post is users


    data = {

    }
    return render(request, "teacher_forum/update.html", data)
