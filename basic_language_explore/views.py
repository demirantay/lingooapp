# Main Imports

# Django Imports
from django.shortcuts import render, get_object_or_404, HttpResponse
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.core.files import File
from django.contrib.auth.models import User

# My Module Imports
from .models import BasicLanguageCourse, Student, Language
from profile_settings.models import BasicUserProfile
from teacher_authentication.models import TeacherUserProfile
from utils.session_utils import get_current_user, get_current_user_profile
from utils.session_utils import get_current_teacher_user_profile
from utils.access_control import delete_teacher_user_session


def basic_language_explore(request, speaker_language):
    """
    In this page the users can explore different kind of languages and enroll
    in them to learn those language courses.
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

    # Get all of the courses
    try:
        all_courses = BasicLanguageCourse.objects.filter(
            course_speakers_language=speaker_language
        )
    except ObjectDoesNotExist:
        all_courses = None

    # course is_enrolled dictionary for every course
    try:
        current_users_students = Student.objects.filter(
            basic_user_profile=current_basic_user_profile
        )
    except ObjectDoesNotExist:
        current_users_students = None

    course_enrollment = {}
    for student in current_users_students:
        for course in all_courses:
            if student.course == course:
                course_enrollment[course.id] = True
            else:
                continue

    # course active learners count
    course_learners_count = {}
    for course in all_courses:
        course_students = Student.objects.filter(course=course)
        students_count = len(course_students)
        course_learners_count[course.id] = students_count

    data = {
        "current_basic_user": current_basic_user,
        "current_basic_user_profile": current_basic_user_profile,
        "current_teacher_profile": current_teacher_profile,
        "all_courses": all_courses,
        "course_enrollment": course_enrollment,
        "course_learners_count": course_learners_count,
        "speaker_language": speaker_language,
    }

    if current_basic_user == None:
        return HttpResponseRedirect("/auth/login/")
    else:
        return render(request, "basic_language_explore/language_explore.html", data)


def basic_language_explore_info(request, course_language, speakers_language):
    """
    in this page the users can see the specific course page and enroll them
    if they want
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

    # If current course does not exists redirect to 404

    # current course active learners count
    try:
        current_course_learners = Student.objects.filter(course=current_course)
    except ObjectDoesNotExist:
        current_course_learners = None

    current_course_learners_count = len(current_course_learners)

    # Get the current course teachers
    try:
        current_course_teachers = TeacherUserProfile.objects.filter(
            course_language=current_course.course_language,
            course_speakers_language=current_course.course_speakers_language
        )
    except ObjectDoesNotExist:
        current_course_teachers = None

    # Get the current student
    try:
        current_student = Student.objects.get(
            basic_user_profile=current_basic_user_profile,
            course=current_course
        )
    except ObjectDoesNotExist:
        current_student = None

    if current_student == None:
        is_enrolled = False
    else:
        is_enrolled = True

    # Get the current lanuguage
    try:
        current_language = Language.objects.get(name=current_course.course_language)
    except ObjectDoesNotExist:
        current_language = None

    # Enroll in course form processing
    if request.POST.get("basic_course_enroll_submit_btn"):
        # check if the user is alredy enrolled in this course
        # if not then enroll her
        if current_student == None:
            # enroll the student than redirect
            new_student = Student(
                langauge=current_language,
                basic_user_profile=current_basic_user_profile,
                course=current_course
            )
            new_student.save()
            return HttpResponseRedirect(
                "/home/" + current_course.course_language + "/"
                + current_course.course_speakers_language + "/"
            )
        else:
            return HttpResponseRedirect(
                "/home/" + current_course.course_language + "/"
                + current_course.course_speakers_language + "/"
            )

    data = {
        "current_basic_user": current_basic_user,
        "current_basic_user_profile": current_basic_user_profile,
        "current_teacher_profile": current_teacher_profile,
        "current_course": current_course,
        "current_course_learners_count": current_course_learners_count,
        "current_course_teachers": current_course_teachers,
        "is_enrolled": is_enrolled,
    }

    if current_basic_user == None:
        return HttpResponseRedirect("/auth/login/")
    else:
        return render(request, "basic_language_explore/info.html", data)
