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
from .models import TeacherLanguageCourse, CourseStatusUpdate
from utils.session_utils import get_current_user, get_current_user_profile
from utils.session_utils import get_current_teacher_user_profile


def teacher_course_overview(request):
    """
    in this view the teachers can see a overview of the languages courses
    that are being developed
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

    # Getting all the language courses
    try:
        all_teacher_courses = TeacherLanguageCourse.objects.all()
    except ObjectDoesNotExist:
        all_teacher_courses = None

    # Getting course contributers count
    course_contributers = {}
    for course in all_teacher_courses:
        contributers = TeacherUserProfile.objects.filter(
            course_language=course.course_language,
            course_speakers_language=course.course_speakers_language
        )
        contributer_count = 0
        for contributer in contributers:
            contributer_count += 1
        course_contributers[course.id] = contributer_count

    data = {
        "current_basic_user": current_basic_user,
        "current_basic_user_profile": current_basic_user_profile,
        "current_teacher_profile": current_teacher_profile,
        "all_teacher_courses": all_teacher_courses,
        "course_contributers": course_contributers,
    }

    if "teacher_user_logged_in" in request.session:
        return render(request, "teacher_language_explore/course_overview.html", data)
    else:
        return HttpResponseRedirect("/")


def teacher_course_status(request, language, speakers_language):
    """
    in this view the teachers can see the status of the other courses
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

    # Getting the current page course
    try:
        current_course = TeacherLanguageCourse.objects.get(
            course_language=language,
            course_speakers_language=speakers_language
        )
    except ObjectDoesNotExist:
        current_course = None

    # Getting all the course contributors
    try:
        current_course_contributors = TeacherUserProfile.objects.filter(
            course_language=language,
            course_speakers_language=speakers_language
        )
    except ObjectDoesNotExist:
        current_course_contributors = None

    # Getting all the course status
    try:
        current_course_status_updates = CourseStatusUpdate.objects.filter(
            course=current_course
        )
    except ObjectDoesNotExist:
        current_course_status_updates = None

    data = {
        "current_basic_user": current_basic_user,
        "current_basic_user_profile": current_basic_user_profile,
        "current_teacher_profile": current_teacher_profile,
        "current_course": current_course,
        "current_course_contributors": current_course_contributors,
        "current_course_status_updates": current_course_status_updates,
    }

    if "teacher_user_logged_in" in request.session:
        return render(request, "teacher_language_explore/course_status.html", data)
    else:
        return HttpResponseRedirect("/")


def teacher_course_status_update(request):
    """
    in this view the teacher can update the course they are in
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

    # A0 Progress form processing
    if request.POST.get("teacher_course_status_a0_progress_submit_btn"):
        progress_amount = request.POST.get("progress_amount")
        # get the current course and create a new status model record
        course = current_teacher_profile.teacher_course
        course.a0 = progress_amount
        course.save()
        return HttpResponseRedirect("/teacher/course/status/update/")

    # A1 Progress form processing
    if request.POST.get("teacher_course_status_a1_progress_submit_btn"):
        progress_amount = request.POST.get("progress_amount")
        # get the current course and create a new status model record
        course = current_teacher_profile.teacher_course
        course.a1 = progress_amount
        course.save()
        return HttpResponseRedirect("/teacher/course/status/update/")

    # A2 Progress form processing
    if request.POST.get("teacher_course_status_a2_progress_submit_btn"):
        progress_amount = request.POST.get("progress_amount")
        # get the current course and create a new status model record
        course = current_teacher_profile.teacher_course
        course.a2 = progress_amount
        course.save()
        return HttpResponseRedirect("/teacher/course/status/update/")

    # B1 Progress form processing
    if request.POST.get("teacher_course_status_b1_progress_submit_btn"):
        progress_amount = request.POST.get("progress_amount")
        # get the current course and create a new status model record
        course = current_teacher_profile.teacher_course
        course.b1 = progress_amount
        course.save()
        return HttpResponseRedirect("/teacher/course/status/update/")

    # B2 Progress form processing
    if request.POST.get("teacher_course_status_b2_progress_submit_btn"):
        progress_amount = request.POST.get("progress_amount")
        # get the current course and create a new status model record
        course = current_teacher_profile.teacher_course
        course.b2 = progress_amount
        course.save()
        return HttpResponseRedirect("/teacher/course/status/update/")

    # C1 Progress form processing
    if request.POST.get("teacher_course_status_c1_progress_submit_btn"):
        progress_amount = request.POST.get("progress_amount")
        # get the current course and create a new status model record
        course = current_teacher_profile.teacher_course
        course.c1 = progress_amount
        course.save()
        return HttpResponseRedirect("/teacher/course/status/update/")

    # Getting all of the status updates
    try:
        all_status_updates = CourseStatusUpdate.objects.filter(
            course=current_teacher_profile.teacher_course
        )
    except ObjectDoesNotExist:
        all_status_updates = None

    # Status update form processing
    if request.POST.get("teacher_course_status_update_submit_btn"):
        status_title = request.POST.get("status_title")
        status_content = request.POST.get("status_content")
        # create a new status
        new_status_update = CourseStatusUpdate(
            course=current_teacher_profile.teacher_course,
            teacher=current_teacher_profile,
            title=status_title,
            content=status_content
        )
        new_status_update.save()
        return HttpResponseRedirect("/teacher/course/status/update/")

    data = {
        "current_basic_user": current_basic_user,
        "current_basic_user_profile": current_basic_user_profile,
        "current_teacher_profile": current_teacher_profile,
        "all_status_updates": all_status_updates,
    }

    if "teacher_user_logged_in" in request.session:
        return render(request, "teacher_language_explore/course_status_update_form.html", data)
    else:
        return HttpResponseRedirect("/")
