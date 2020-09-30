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
from basic_vocab_container.models import BasicVocabularyContainer
from basic_vocab_container.models import StudentVocabProgress
from basic_language_explore.models import BasicLanguageCourse, Student
from utils.session_utils import get_current_user, get_current_user_profile
from utils.session_utils import get_current_teacher_user_profile
from utils.access_control import delete_teacher_user_session


def index(request):
    """index will redirect the page to `learn` if user is logged in"""
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

    # If the user has the courses parameter info redirect to that
    # courses home page with the parameters
    if "current_course_langauge" in request.session:
        return HttpResponseRedirect(
            "/home/" + request.session["current_course_langauge"] + "/" +
            request.session["current_course_speakers_language"] + "/"
        )

    # This part of redirection is to see for some reason if the user has
    # enrolled in a course but the sessions are for some reson not set
    try:
        current_student_profiles = Student.objects.filter(
            basic_user_profile=current_basic_user_profile
        )
    except ObjectDoesNotExist:
        current_student_profiles = None

    if len(current_student_profiles) == 0:
        pass
    else:
        for student in current_student_profiles:
            if student.course == None or bool(student.course) == False:
                current_student = None
            else:
                current_student = student
        # current_student = current_student_profiles[0]
        if current_student == None:
            pass
        else:
            request.session["current_course_langauge"] = current_student.course.course_language
            request.session["current_course_speakers_language"] = current_student.course.course_speakers_language
            return HttpResponseRedirect("/")

    data = {
        "current_basic_user": current_basic_user,
        "current_basic_user_profile": current_basic_user_profile,
        "current_teacher_profile": current_teacher_profile,
    }

    if current_basic_user == None:
        return render(request, "home/landing_page_v2.html", data)
    else:
        return render(request, "home/placeholder_home.html", data)


def learn_index(request, course_language, speakers_language):
    """
    in this page the user can switch their student account and view their main
    learning tree this is the main deal
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

    # Get the current course
    try:
        current_course = BasicLanguageCourse.objects.get(
            course_language=course_language,
            course_speakers_language=speakers_language
        )
    except ObjectDoesNotExist:
        current_course = None

    if current_course == None:
        return HttpResponseRedirect("/")

    # Get the current student
    try:
        current_student = Student.objects.get(
            basic_user_profile=current_basic_user_profile,
            course=current_course
        )
    except ObjectDoesNotExist:
        current_student = None

    if current_student == None:
        return HttpResponseRedirect("/")

    # Add the session
    request.session["current_course_langauge"] = current_student.course.course_language
    request.session["current_course_speakers_language"] = current_student.course.course_speakers_language

    # Get the words learned for the current_students course progress
    try:
        current_words = StudentVocabProgress.objects.filter(
            student=current_student,
            is_learned=True,
        )
    except ObjectDoesNotExist:
        current_words = None

    # Get all of current users student records
    try:
        all_current_user_student_profiles = Student.objects.filter(
            basic_user_profile=current_basic_user_profile,
        )
    except ObjectDoesNotExist:
        all_current_user_student_profiles = None

    # Current Student A0 progress
    a0_progress = 0
    a1_progress = 0
    a2_progress = 0
    b1_progress = 0
    b2_progress = 0
    c1_progress = 0
    advanced_progress = 0

    for word in current_words:
        if word.vocab_container_word.level == "a0":
            a0_progress += 1
        elif word.vocab_container_word.level == "a1":
            a1_progress += 1
        elif word.vocab_container_word.level == "a2":
            a2_progress += 1
        elif word.vocab_container_word.level == "b1":
            b1_progress += 1
        elif word.vocab_container_word.level == "b2":
            b2_progress += 1
        elif word.vocab_container_word.level == "c1":
            c1_progress += 1
        elif word.vocab_container_word.level == "advanced":
            advanced_progress += 1
        else:
            continue

    is_a0_done = False
    is_a1_done = False
    is_a2_done = False
    is_b1_done = False
    is_b2_done = False
    is_c1_done = False
    is_advanced_done = False

    # is a0 done
    if a0_progress >= 100:
        is_a0_done = True

    # is a1 done
    if a1_progress >= 500:
        is_a1_done = True

    # is a2 done
    if a2_progress >= 1000:
        is_a2_done = True

    # is b1 done
    if b1_progress >= 2000:
        is_b1_done = True

    # is b2 done
    if b2_progress >= 4000:
        is_b2_done = True

    # is c1 done
    if c1_progress >= 8000:
        is_c1_done = True

    # is advanced done
    if advanced_progress >= 16000:
        is_advanced_done = True

    data = {
        "current_basic_user": current_basic_user,
        "current_basic_user_profile": current_basic_user_profile,
        "current_teacher_profile": current_teacher_profile,
        "words_learned": len(current_words),
        "course_language": course_language,
        "speakers_language": speakers_language,
        "current_student": current_student,
        "all_current_user_student_profiles": all_current_user_student_profiles,
        "a0_progress": a0_progress,
        "a1_progress": a1_progress,
        "a2_progress": a2_progress,
        "b1_progress": b1_progress,
        "b2_progress": b2_progress,
        "c1_progress": c1_progress,
        "advanced_progress": advanced_progress,
        "is_a0_done": is_a0_done,
        "is_a1_done": is_a1_done,
        "is_a2_done": is_a2_done,
        "is_b1_done": is_b1_done,
        "is_b2_done": is_b2_done,
        "is_c1_done": is_c1_done,
        "is_advanced_done": is_advanced_done,
    }

    if current_basic_user == None:
        return HttpResponseRedirect("/auth/login/")
    else:
        return render(request, "home/learning_tree.html", data)


def under_construction(request):
    """under constrction page"""

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

    data = {
        "current_basic_user": current_basic_user,
        "current_basic_user_profile": current_basic_user_profile,
    }

    return render(request, "redirect_pages/under_construction.html", data)


def error_404(request):
    """error 404 not existing page"""
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

    data = {
        "current_basic_user": current_basic_user,
        "current_basic_user_profile": current_basic_user_profile,
    }

    return render(request, "redirect_pages/error_404.html", data)
