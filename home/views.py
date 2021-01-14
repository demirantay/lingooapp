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
from basic_language_explore.models import BasicLanguageCourse, Student, Language
from basic_notifications.models import NotificationBase, AnnouncementIsRead
from basic_notifications.models import AnnouncementNotification

from utils.session_utils import get_current_user, get_current_user_profile
from utils.session_utils import get_current_teacher_user_profile
from utils.access_control import delete_teacher_user_session
from utils.notification_utils import get_unread_notifications


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
        return render(request, "home/landing_page_v4.html", data)
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

    # Getting, if there are any unread notifications of the current user
    has_unread_notifications = get_unread_notifications(
        NotificationBase,
        current_basic_user_profile,
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

    # Code logic for `course has not been built yet message`

    try:
        all_course_words = BasicVocabularyContainer.objects.filter(
            course=current_course
        )
    except ObjectDoesNotExist:
        all_course_words = None

    # Course Words Count for redirection
    a0_words = 0
    a1_words = 0
    a2_words = 0
    b1_words = 0
    b2_words = 0
    c1_words = 0
    advanced_words = 0

    for word in all_course_words:
        if word.level == "a0":
            a0_words += 1
        elif word.level == "a1":
            a1_words += 1
        elif word.level == "a2":
            a2_words += 1
        elif word.level == "b1":
            b1_words += 1
        elif word.level == "b2":
            b2_words += 1
        elif word.level == "c1":
            c1_words += 1
        elif word.level == "advanced":
            advanced_words += 1

    a0_course_not_built = False
    a1_course_not_built = False
    a2_course_not_built = False
    b1_course_not_built = False
    b2_course_not_built = False
    c1_course_not_built = False
    advanced_course_not_built = False

    if a0_words < 100:
        a0_course_not_built = True
    elif a1_words < 500:
        a1_course_not_built = True
    elif a2_words < 1000:
        a2_course_not_built = True
    elif b1_words < 2000:
        b1_course_not_built = True
    elif b2_words < 4000:
        b2_course_not_built = True
    elif c1_words < 8000:
        c1_course_not_built = True
    elif advanced_words < 16000:
        advanced_course_not_built = True

    # ------------

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

    # Getting the data for the ranking feature on the homepage
    try:
        current_langauge = Language.objects.get(
            name=current_course.course_language
        )
    except ObjectDoesNotExist:
        current_langauge = None

    try:
        all_student_profiles = Student.objects.filter(
            langauge=current_langauge
        ).order_by("-xp")
    except ObjectDoesNotExist:
        all_student_profiles = None

    '''
    # Get all the ranks for the bottom
    rankings = {}
    rank = 1
    for student in all_student_profiles:
        rankings[student.id] = rank
        rank += 1

    current_student_rank = list(all_student_profiles).index(current_student)

    ranking_box = []

    # add the upper ranks
    if current_student_rank > 1:
        ranking_box.append(all_student_profiles[current_student_rank - 2])
        ranking_box.append(all_student_profiles[current_student_rank - 1])
    elif current_student_rank == 1:
        ranking_box.append(all_student_profiles[current_student_rank - 1])

    # add the current student rank
    ranking_box.append(all_student_profiles[current_student_rank])

    # add the lower ranks
    if len(all_student_profiles) - (current_student_rank + 1) >= 2:
        ranking_box.append(all_student_profiles[current_student_rank + 1])
        ranking_box.append(all_student_profiles[current_student_rank + 2])
    elif len(all_student_profiles) - (current_student_rank + 1) == 1:
        ranking_box.append(all_student_profiles[current_student_rank + 1])
    '''

    # Getting the announcements that the current user has not read
    try:
        all_announcaments = AnnouncementNotification.objects.all(
        ).order_by("-id")
    except ObjectDoesNotExist:
        all_announcaments = None

    # Get the current users read(dismissed announcaments)
    try:
        user_announcement_dismiss_objcects = AnnouncementIsRead.objects.filter(
            user_profile=current_basic_user_profile
        )
        read_announcaments = []
        for announcement in user_announcement_dismiss_objcects:
            read_announcaments.append(announcement.announcement)
    except ObjectDoesNotExist:
        user_announcement_dismiss_objcects = None
        read_announcaments = []

    # Create a new array that is filled with the announcaments that are
    # not dissmised by the current user
    filtered_announcaments = []

    for announcament in list(all_announcaments):
        if announcament in read_announcaments:
            print("this announcament is read")
        else:
            filtered_announcaments.append(announcament)

    # Announcament dismiss (read) forum processing
    if request.POST.get("notification_announcament_dismiss_clicked"):
        hidden_announcament_id = request.POST.get("hidden_announcament_id")
        hidden_announcament = AnnouncementNotification.objects.get(
            id=hidden_announcament_id
        )
        # create the new annoucment is read model record
        new_notification_dismiss = AnnouncementIsRead(
            announcement=hidden_announcament,
            user_profile=current_basic_user_profile,
        )
        new_notification_dismiss.save()
        return HttpResponseRedirect("/")

    data = {
        "current_basic_user": current_basic_user,
        "current_basic_user_profile": current_basic_user_profile,
        "current_teacher_profile": current_teacher_profile,
        "has_unread_notifications": has_unread_notifications,
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

        "a0_course_not_built": a0_course_not_built,
        "a1_course_not_built": a1_course_not_built,
        "a2_course_not_built": a2_course_not_built,
        "b1_course_not_built": b1_course_not_built,
        "b2_course_not_built": b2_course_not_built,
        "c1_course_not_built": c1_course_not_built,
        "advanced_course_not_built": advanced_course_not_built,

        "filtered_announcaments": filtered_announcaments,
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
