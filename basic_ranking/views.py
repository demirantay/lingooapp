# Main Imports

# Django Imports
from django.shortcuts import render, get_object_or_404, HttpResponse
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.core.files import File
from django.contrib.auth.models import User
from django.utils import timezone

# My Module ImportsImports
from profile_settings.models import BasicUserProfile
from teacher_authentication.models import TeacherUserProfile
from basic_language_explore.models import BasicLanguageCourse, Student, Language

from utils.session_utils import get_current_user, get_current_user_profile
from utils.session_utils import get_current_teacher_user_profile
from utils.access_control import delete_teacher_user_session


def ranking_overview(request, page):
    """
    in this page the users can see all of the rankings
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

    # Get the current user's student profiles
    try:
        current_user_student_profiles = Student.objects.filter(
            basic_user_profile=current_basic_user_profile
        ).order_by("-xp")
    except ObjectDoesNotExist:
        current_user_student_profiles = None

    # Get all of the student profiles for overview
    # At every page there will be 80 entries so always multiply it by that and
    # then reduce your objects
    current_page = page
    previous_page = page-1
    next_page = page+1

    post_records_starting_point = current_page * 1000
    post_records_ending_point = post_records_starting_point + 1000

    try:
        all_student_profiles = Student.objects.all(
        ).order_by("-xp")
    except ObjectDoesNotExist:
        all_student_profiles = None

    filtered = all_student_profiles[post_records_starting_point:post_records_ending_point]

    # Get the ranks for the top part where the curernt users ranks show up
    current_user_ranks = {}

    for student in current_user_student_profiles:
        current_user_ranks[student.id] = list(all_student_profiles).index(student) + 1

    # Get all the ranks for the bottom
    rankings = {}
    rank = post_records_starting_point + 1
    for student in filtered:
        rankings[student.id] = rank
        rank += 1

    data = {
        "current_basic_user": current_basic_user,
        "current_basic_user_profile": current_basic_user_profile,
        "current_teacher_profile": current_teacher_profile,
        "current_user_student_profiles": current_user_student_profiles,
        "all_student_profiles": all_student_profiles,
        "rankings": rankings,
        "current_user_ranks": current_user_ranks,
        "current_page": current_page,
        "previous_page": previous_page,
        "next_page": next_page,
        "filtered": filtered,
    }

    if current_basic_user == None:
        return HttpResponseRedirect("/auth/login/")
    else:
        return render(request, "basic_ranking/overview.html", data)


def category_ranking(request, language, page):
    """
    In this page the users can see the ranking of different language courses
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

    # Get the current language of the page
    try:
        current_langauge = Language.objects.get(name=language)
    except ObjectDoesNotExist:
        current_langauge = None

    if current_langauge == None:
        return HttpResponseRedirect("/")

    # Get all of the current students for navigation
    try:
        current_user_student_profiles = Student.objects.filter(
            basic_user_profile=current_basic_user_profile
        ).order_by("-xp")
    except ObjectDoesNotExist:
        current_user_student_profiles = None

    # Get all of the students with the current language of the category
    # At every page there will be 80 entries so always multiply it by that and
    # then reduce your objects
    current_page = page
    previous_page = page-1
    next_page = page+1

    post_records_starting_point = current_page * 1000
    post_records_ending_point = post_records_starting_point + 1000

    try:
        all_student_profiles = Student.objects.filter(
            langauge=current_langauge
        ).order_by("-xp")
    except ObjectDoesNotExist:
        all_student_profiles = None

    filtered = all_student_profiles[post_records_starting_point:post_records_ending_point]

    # Get all the ranks for the bottom
    rankings = {}
    rank = post_records_starting_point + 1
    for student in filtered:
        rankings[student.id] = rank
        rank += 1

    # Get the rank of the current student
    for student in current_user_student_profiles:
        if student.langauge.name == language:
            current_student = student
            break

    current_student_rank = list(all_student_profiles).index(current_student) + 1

    data = {
        "current_basic_user": current_basic_user,
        "current_basic_user_profile": current_basic_user_profile,
        "current_teacher_profile": current_teacher_profile,
        "current_page": current_page,
        "previous_page": previous_page,
        "next_page": next_page,
        "all_student_profiles": all_student_profiles,
        "current_user_student_profiles": current_user_student_profiles,
        "page_langauge": language,
        "rankings": rankings,
        "filtered": filtered,
        "current_student_rank": current_student_rank,
    }

    if current_basic_user == None:
        return HttpResponseRedirect("/auth/login/")
    else:
        return render(request, "basic_ranking/category_ranking.html", data)
