# Main Imports

# Django Imports
from django.shortcuts import render, get_object_or_404, HttpResponse
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.core.files import File
from django.contrib.auth.models import User

# My Module Imports
from profile_settings.models import BasicUserProfile
from teacher_authentication.models import TeacherUserProfile
from basic_language_explore.models import Student, BasicLanguageCourse, Language
from basic_vocab_container.models import StudentVocabProgress
from forum.models import ForumPost
from basic_voting_sys.models import BillVote
from utils.session_utils import get_current_user, get_current_user_profile
from utils.session_utils import get_other_user, get_other_user_profile
from utils.session_utils import get_current_teacher_user_profile
from utils.access_control import delete_teacher_user_session


def profile_overview(request, course_language, speakers_language):
    """
    Users can see their own profile pages from here.
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

    # Get the current users Student Profiles
    try:
        all_student_profiles = Student.objects.filter(
            basic_user_profile=current_basic_user_profile
        )
    except ObjectDoesNotExist:
        all_student_profiles = None

    # Get the current course
    try:
        current_course = BasicLanguageCourse.objects.get(
            course_language=course_language,
            course_speakers_language=speakers_language,
        )
    except ObjectDoesNotExist:
        current_course = None

    # Get the current student profile
    try:
        current_student_profile = Student.objects.get(
            basic_user_profile=current_basic_user_profile,
            course=current_course,
        )
    except ObjectDoesNotExist:
        current_student_profile = None

    # If page course does not exists redirect to home page
    # (the initial redirect to this view from the left navigation will
    # always have a "foo/foo" not existent current course type because it is
    # cumbersome to pass neccessary variables for every view that extends
    # from that base. so instead all of them will redirect to a an not existing
    # /foo/foo/ and then the code below will redierct the user to current
    # language that is stored in the session) if even those variables are not
    # existnet too just redirect the user to the home page.
    if current_student_profile == None:
        try:
            session_lang = request.session["current_course_langauge"]
            session_speakers_lang = request.session["current_course_speakers_language"]
        except ObjectDoesNotExist:
            session_lang = None
            session_speakers_lang = None

        if session_lang == None or session_speakers_lang == None:
            return HttpResponseRedirect("/")

        return HttpResponseRedirect(
            "/profile/" + session_lang + "/" +  session_speakers_lang + "/"
        )

    # Get the current user learned words
    # Get the words learned for the current_students course progress
    try:
        current_words = StudentVocabProgress.objects.filter(
            student=current_student_profile,
            is_learned=True,
        )
    except ObjectDoesNotExist:
        current_words = None

    # Get current users forum posts
    try:
        current_language = Language.objects.get(
            name=current_student_profile.course.course_language
        )
        current_forum_posts = ForumPost.objects.filter(
            user_profile=current_basic_user_profile,
            language=current_language
        )
    except ObjectDoesNotExist:
        current_language = None
        current_forum_posts = None

    # Get current users bill votes
    try:
        current_bill_votes = BillVote.objects.filter(
            voter=current_basic_user_profile
        )
    except ObjectDoesNotExist:
        current_bill_votes = None

    data = {
        "current_basic_user": current_basic_user,
        "current_basic_user_profile": current_basic_user_profile,
        "current_teacher_profile": current_teacher_profile,
        "all_student_profiles": all_student_profiles,
        "current_student_profile": current_student_profile,
        "current_words_learned": len(current_words),
        "current_forum_posts": len(current_forum_posts),
        "current_bill_votes": len(current_bill_votes),
    }

    if current_basic_user == None:
        return HttpResponseRedirect("/auth/login/")
    else:
        return render(request, "profile/new_profile.html", data)


def other_user_profile_overview(request, other_user_username):
    """
    The users can see other users profile pages (not their own profile)
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

    # Get the other user
    other_basic_user = get_other_user(
        request,
        other_user_username,
        User,
        ObjectDoesNotExist
    )

    other_basic_user_profile = get_other_user_profile(
        request,
        other_user_username,
        User,
        BasicUserProfile,
        ObjectDoesNotExist
    )

    if other_basic_user == None or other_basic_user_profile == None:
        return HttpResponseRedirect("/404/")

    data = {
        "current_basic_user": current_basic_user,
        "current_basic_user_profile": current_basic_user_profile,
        "current_teacher_profile": current_teacher_profile,
        "other_basic_user": other_basic_user,
        "other_basic_user_profile": other_basic_user_profile,
    }

    if current_basic_user == None:
        return HttpResponseRedirect("/auth/login/")
    else:
        return render(request, "profile/other_user_profile_overview.html", data)
