# Main Imports

# Django Imports
from django.shortcuts import render, get_object_or_404, HttpResponse
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

# My Module Imports
from profile_settings.models import BasicUserProfile
from teacher_authentication.models import TeacherUserProfile
from utils.session_utils import get_current_user, get_current_user_profile
from utils.session_utils import get_current_teacher_user_profile

from .models import TeacherReadingLesson, TeacherReadingLessonSentence
from .models import TeacherReadingLessonSentenceTolerance


def teacher_reading_build(request, course_language, course_speaker_language):
    """
    in this page the teacher can build the neccessary reading lessons
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

    # Adding a new lesson to the teacher course form processing
    empty_lesson_name = False

    if request.POST.get("teacher_reading_builder_lesson_add_button"):
        lesson_name = request.POST.get("lesson_name")
        lesson_level = request.POST.get("lesson_level")

        if bool(lesson_name) == False or lesson_name == "":
            empty_lesson_name = True
        else:
            new_lesson = TeacherReadingLesson(
                course=current_teacher_profile.teacher_course,
                teacher=current_teacher_profile,
                title=lesson_name,
                level=lesson_level,
            )
            new_lesson.save()
            return HttpResponseRedirect(
                "/teacher/reading/build/" + course_language +
                "/" + course_speaker_language + "/"
            )

    # Getting all of the lessons, sentences and tolerances s of the
    # current course
    try:
        a0_lessons = TeacherReadingLesson.objects.filter(
            course=current_teacher_profile.teacher_course,
            level="a0"
        ).order_by("id")
    except ObjectDoesNotExist:
        a0_lessons = None

    try:
        a1_lessons = TeacherReadingLesson.objects.filter(
            course=current_teacher_profile.teacher_course,
            level="a1"
        ).order_by("id")
    except ObjectDoesNotExist:
        a1_lessons = None

    try:
        a2_lessons = TeacherReadingLesson.objects.filter(
            course=current_teacher_profile.teacher_course,
            level="a2"
        ).order_by("id")
    except ObjectDoesNotExist:
        a2_lessons = None

    try:
        b1_lessons = TeacherReadingLesson.objects.filter(
            course=current_teacher_profile.teacher_course,
            level="b1"
        ).order_by("id")
    except ObjectDoesNotExist:
        b1_lessons = None

    try:
        b2_lessons = TeacherReadingLesson.objects.filter(
            course=current_teacher_profile.teacher_course,
            level="b2"
        ).order_by("id")
    except ObjectDoesNotExist:
        b2_lessons = None

    try:
        c1_lessons = TeacherReadingLesson.objects.filter(
            course=current_teacher_profile.teacher_course,
            level="c1"
        ).order_by("id")
    except ObjectDoesNotExist:
        c1_lessons = None

    try:
        advanced_lessons = TeacherReadingLesson.objects.filter(
            course=current_teacher_profile.teacher_course,
            level="advanced"
        ).order_by("id")
    except ObjectDoesNotExist:
        advanced_lessons = None

    # getting the lesson sentence cells
    # a0 lessons sentences
    a0_lesson_sentences = {}
    for lesson in a0_lessons:
        a0_lesson_sentences[lesson.id] = []
        sentences = TeacherReadingLessonSentence.objects.filter(
            lesson=lesson
        ).order_by("id")
        for sentence in sentences:
            a0_lesson_sentences[lesson.id].append(sentence)

    # getting a1 lessons sentences
    a1_lesson_sentences = {}
    for lesson in a1_lessons:
        a1_lesson_sentences[lesson.id] = []
        sentences = TeacherReadingLessonSentence.objects.filter(
            lesson=lesson
        ).order_by("id")
        for sentence in sentences:
            a1_lesson_sentences[lesson.id].append(sentence)

    # getting a2 lessons sentences
    a2_lesson_sentences = {}
    for lesson in a2_lessons:
        a2_lesson_sentences[lesson.id] = []
        sentences = TeacherReadingLessonSentence.objects.filter(
            lesson=lesson
        ).order_by("id")
        for sentence in sentences:
            a2_lesson_sentences[lesson.id].append(sentence)

    # getting b1 lessons sentences
    b1_lesson_sentences = {}
    for lesson in b1_lessons:
        b1_lesson_sentences[lesson.id] = []
        sentences = TeacherReadingLessonSentence.objects.filter(
            lesson=lesson
        ).order_by("id")
        for sentence in sentences:
            b1_lesson_sentences[lesson.id].append(sentence)

    # getting b2 lessons sentences
    b2_lesson_sentences = {}
    for lesson in b2_lessons:
        b2_lesson_sentences[lesson.id] = []
        sentences = TeacherReadingLessonSentence.objects.filter(
            lesson=lesson
        ).order_by("id")
        for sentence in sentences:
            b2_lesson_sentences[lesson.id].append(sentence)

    # getting c1 lessons sentences
    c1_lesson_sentences = {}
    for lesson in c1_lessons:
        c1_lesson_sentences[lesson.id] = []
        sentences = TeacherReadingLessonSentence.objects.filter(
            lesson=lesson
        ).order_by("id")
        for sentence in sentences:
            c1_lesson_sentences[lesson.id].append(sentence)

    # getting advanced lessons sentences
    advanced_lesson_sentences = {}
    for lesson in advanced_lessons:
        advanced_lesson_sentences[lesson.id] = []
        sentences = TeacherReadingLessonSentence.objects.filter(
            lesson=lesson
        ).order_by("id")
        for sentence in sentences:
            advanced_lesson_sentences[lesson.id].append(sentence)

    # Automation for the teacher course

    data = {
        "current_basic_user": current_basic_user,
        "current_basic_user_profile": current_basic_user_profile,
        "current_teacher_profile": current_teacher_profile,
        "empty_lesson_name": empty_lesson_name,
        "a0_lessons": a0_lessons,
        "a1_lessons": a1_lessons,
        "a2_lessons": a2_lessons,
        "b1_lessons": b1_lessons,
        "b2_lessons": b2_lessons,
        "c1_lessons": c1_lessons,
        "advanced_lessons": advanced_lessons,
        "a0_lesson_sentences": a0_lesson_sentences,
        "a1_lesson_sentences": a1_lesson_sentences,
        "a2_lesson_sentences": a2_lesson_sentences,
        "b1_lesson_sentences": b1_lesson_sentences,
        "b2_lesson_sentences": b2_lesson_sentences,
        "c1_lesson_sentences": c1_lesson_sentences,
        "advanced_lesson_sentences": advanced_lesson_sentences,
    }

    if "teacher_user_logged_in" in request.session:
        return render(request, "teacher_reading_builder/build.html", data)
    else:
        return HttpResponseRedirect("/")


def teacher_reading_update(request, id):
    """
    in this page the teachers can update and edit a lesson sentence
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

    # Get the current Lesson Sentence Object
    try:
        current_lesson_sentence = TeacherReadingLessonSentence.objects.get(
            id=id
        )
    except ObjectDoesNotExist:
        current_lesson_sentence = None

    # Get all of the tolerance data of the cucrrent lesson sentence
    try:
        current_sentence_tolerances = TeacherReadingLessonSentenceTolerance.objects.filter(
            lesson_sentence=current_lesson_sentence
        )
    except ObjectDoesNotExist:
        current_sentence_tolerances = None

    # check if the current sentences course is matching the current teacher
    # if not then redirect to home

    # !!!!!!!!!!!!!!!!!!!!!!! ^^^^^^^^^^^^^^^^

    # Edit/Update the question, answer prompts
    empty_input = False

    if request.POST.get("teacher_reading_sentence_update_submit_btn"):
        new_question_prompt = request.POST.get("new_question_prompt")
        new_answer = request.POST.get("new_answer")

        if bool(new_question_prompt) == False or new_question_prompt == "" or \
           bool(new_answer) == False or new_answer == "":
            empty_input = True
        else:
            current_lesson_sentence.question_prompt = new_question_prompt
            current_lesson_sentence.answer = new_answer
            current_lesson_sentence.save()
            return HttpResponseRedirect(
                "/teacher/reading/update/" + str(id) + "/"
            )

    # Typo tolerance addition form processing
    if request.POST.get("teacher_reading_tolerance_update_submit_btn"):
        tolerance = request.POST.get("tolerance")

        if bool(tolerance) == False or tolerance == "":
            empty_input = True
        else:
            new_tolerance = TeacherReadingLessonSentenceTolerance(
                lesson_sentence=current_lesson_sentence,
                tolerated_answer=tolerance
            )
            new_tolerance.save()
            return HttpResponseRedirect(
                "/teacher/reading/update/" + str(id) + "/"
            )

    # Delete the sentence form processing
    if request.POST.get("teacher_reading_sentence_delete_submit_btn"):
        # delete the tolerances
        current_sentence_tolerances.delete()
        # delete the sentence
        current_lesson_sentence.delete()
        return HttpResponseRedirect(
            "/teacher/reading/build/" +
            current_teacher_profile.teacher_course.course_language + "/" +
            current_teacher_profile.teacher_course.course_speakers_language
            + "/"
        )

    data = {
        "current_basic_user": current_basic_user,
        "current_basic_user_profile": current_basic_user_profile,
        "current_teacher_profile": current_teacher_profile,
        "id": id,
        "current_lesson_sentence": current_lesson_sentence,
        "empty_input": empty_input,
        "current_sentence_tolerances": current_sentence_tolerances,
    }

    if "teacher_user_logged_in" in request.session:
        return render(request, "teacher_reading_builder/update.html", data)
    else:
        return HttpResponseRedirect("/")


def teacher_reading_add_sentence(request):
    """
    in this page the teachers can add sentences to the reading lessons
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

    # Get the current reading lessons for 'select' dropdown
    try:
        all_lessons = TeacherReadingLesson.objects.filter(
            course=current_teacher_profile.teacher_course
        )
    except ObjectDoesNotExist:
        all_lessons = None

    # Add the new lesson form processing
    empty_input = False

    if request.POST.get("teacher_reading_sentence_addition_form_submit_btn"):
        sentence_level = request.POST.get("sentence_level")
        question_prompt = request.POST.get("question_prompt")
        answer = request.POST.get("answer")
        selected_lesson_id = request.POST.get("selected_lesson_id")

        # get the selected lesson
        try:
            selected_lesson = TeacherReadingLesson.objects.get(
                id=selected_lesson_id
            )
        except ObjectDoesNotExist:
            selected_lesson = None

        # check if anything has empty input
        if bool(question_prompt) == False or question_prompt == "" or \
           bool(answer) == False or answer == "":
            empty_input = True
        else:
            new_sentence = TeacherReadingLessonSentence(
                lesson=selected_lesson,
                level=sentence_level,
                question_prompt=question_prompt,
                answer=answer
            )
            new_sentence.save()
            return HttpResponseRedirect(
                "/teacher/reading/build/" +
                current_teacher_profile.teacher_course.course_language + "/" +
                current_teacher_profile.teacher_course.course_speakers_language
                + "/"
            )

    data = {
        "current_basic_user": current_basic_user,
        "current_basic_user_profile": current_basic_user_profile,
        "current_teacher_profile": current_teacher_profile,
        "all_lessons": all_lessons,
        "empty_input": empty_input,
    }

    if "teacher_user_logged_in" in request.session:
        return render(request, "teacher_reading_builder/add_sentence.html", data)
    else:
        return HttpResponseRedirect("/")
