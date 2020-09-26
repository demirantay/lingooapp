# Main Imports
import json

# Django Imports
from django.shortcuts import render, get_object_or_404, HttpResponse
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.core.files import File
from django.contrib.auth.models import User

# My Module ImportsImports
from .models import BasicVocabularyContainer, StudentVocabProgress
from .models import BasicVocabErrorReport
from basic_language_explore.models import BasicLanguageCourse, Student, Language
from profile_settings.models import BasicUserProfile
from teacher_authentication.models import TeacherUserProfile
from utils.session_utils import get_current_user, get_current_user_profile
from utils.session_utils import get_current_teacher_user_profile
from utils.access_control import delete_teacher_user_session


def basic_vocab_learn_start(request, cefr_level, course_language, speakers_langauge):
    """
    in this view the user can see the vocabulary list for the current vocab
    lesson
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

    # Get the current course
    try:
        current_course = BasicLanguageCourse.objects.get(
            course_language=course_language,
            course_speakers_language=speakers_langauge
        )
    except ObjectDoesNotExist:
        current_course = None

    # Get the current student
    try:
        current_student = Student.objects.get(
            basic_user_profile=current_basic_user_profile,
            course=current_course
        )
    except ObjectDoesNotExist:
        current_student = None

    # if the student does not exists for the current course return 404
    # !!!!!!!!!
    # !!!!!!!!!
    # !!!!!!!!!

    # Get the next 10 words to learn and display them to the user
    try:
        all_course_words = BasicVocabularyContainer.objects.filter(
            course=current_course
        )
    except ObjectDoesNotExist:
        all_course_words = None

    # Get the current students progress words
    try:
        current_student_progress = StudentVocabProgress.objects.filter(
            student=current_student
        )
    except ObjectDoesNotExist:
        current_student_progress = None

    # Get the current lessons packs (10) words
    unlearned_words = []
    for word in current_student_progress:
        if word.vocab_container_word.level == cefr_level:
            if word.is_learned == False:
                unlearned_words.append(word)
    lesson_pack = unlearned_words[:10]

    # If the current lesson pack do not serve the lesson
    if len(unlearned_words) < 10:
        return HttpResponseRedirect("/")

    # Based on the current CEFR level update the student progresses word list
    # if there are any additions to the main vocab container

    def update_student_words(level):
        current_progress = []
        for word in current_student_progress:
            if word.vocab_container_word.level == level:
                current_progress.append(word.vocab_container_word)

        leveled_words = []
        for word in all_course_words:
            if word.level == level:
                leveled_words.append(word)

        for word in leveled_words:
            if word in current_progress:
                pass
            else:
                # if word does not exist in current stdent prgoress, add it
                new_progress = StudentVocabProgress(
                    student=current_student,
                    vocab_container_word=word,
                )
                new_progress.save()
                return HttpResponseRedirect(
                    "/vocab/learn/start/" + str(cefr_level) + "/" +
                    str(current_course.course_language) + "/" +
                    str(current_course.course_speakers_language) + "/"
                )

    if cefr_level == "a0":
        '''
        current_a0_progress = []
        for word in current_student_progress:
            if word.vocab_container_word.level == "a0":
                current_a0_progress.append(word.vocab_container_word)

        a0_words = []
        for word in all_course_words:
            if word.level == "a0":
                a0_words.append(word)

        for word in a0_words:
            if word in current_a0_progress:
                pass
            else:
                # if word does not exist in current stdent prgoress, add it
                new_progress = StudentVocabProgress(
                    student=current_student,
                    vocab_container_word=word,
                )
                new_progress.save()'''

        update_student_words("a0")
    elif cefr_level == "a1":
        update_student_words("a1")
    elif cefr_level == "a2":
        update_student_words("a2")
    elif cefr_level == "b1":
        update_student_words("b1")
    elif cefr_level == "b2":
        update_student_words("b2")
    elif cefr_level == "c1":
        update_student_words("c1")
    elif cefr_level == "advanced":
        update_student_words("advanced")
    else:
        pass

    data = {
        "current_basic_user": current_basic_user,
        "current_basic_user_profile": current_basic_user_profile,
        "lesson_pack": lesson_pack,
        "current_course": current_course,
        "cefr_level": cefr_level,
    }

    if current_basic_user == None:
        return HttpResponseRedirect("/auth/login/")
    else:
        return render(request, "basic_vocab_container/learning_start.html", data)


def basic_vocab_learn(request, cefr_level, course_language, speakers_langauge):
    """
    in this view the person can learn new vocabulary on courses
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

    # Get the current course
    try:
        current_course = BasicLanguageCourse.objects.get(
            course_language=course_language,
            course_speakers_language=speakers_langauge
        )
    except ObjectDoesNotExist:
        current_course = None

    # Get the current student
    try:
        current_student = Student.objects.get(
            basic_user_profile=current_basic_user_profile,
            course=current_course
        )
    except ObjectDoesNotExist:
        current_student = None

    # Get the current students progress words
    try:
        current_student_progress = StudentVocabProgress.objects.filter(
            student=current_student
        )
    except ObjectDoesNotExist:
        current_student_progress = None

    # Get the current lessons packs (10) words
    unlearned_words = []
    for word in current_student_progress:
        if word.vocab_container_word.level == cefr_level:
            if word.is_learned == False:
                unlearned_words.append(word)
    lesson_pack = unlearned_words[:10]

    lesson_pack_words = {}
    for word in unlearned_words[:10]:
        lesson_pack_words[word.vocab_container_word.word] = word.vocab_container_word.word_translation

    # If the current lesson pack do not serve the lesson
    if len(unlearned_words) < 10:
        return HttpResponseRedirect("/")

    # If every checkpoint is done and the lessons are learned, update the
    # student progress
    if request.POST.get("vocab_learning_lesson_finish_button"):
        hidden_errors_array = request.POST.get("hidden_errors_array")

        parsed_json = []
        if hidden_errors_array:
            parsed_json = json.loads(hidden_errors_array)
        else:
            parsed_json = []

        # Add the ERRORs
        if bool(parsed_json) == False or parsed_json == {} or parsed_json == []:
            # its empty pass
            pass
        else:
            # Get the current vocab container recrod
            for data in parsed_json:
                for word in unlearned_words[:10]:
                    if data.get("question") == word.vocab_container_word.word:
                        # it matches create a error record
                        new_error = BasicVocabErrorReport(
                            student=current_student,
                            course=current_course,
                            vocab_container=word.vocab_container_word,
                            error_report=data.get("content")
                        )
                        new_error.save()
                    else:
                        pass

        # Make the words learned
        for word in unlearned_words[:10]:
            word.is_learned = True
            word.save()
        return HttpResponseRedirect("/")

    data = {
        "current_basic_user": current_basic_user,
        "current_basic_user_profile": current_basic_user_profile,
        "lesson_pack": lesson_pack,
        "lesson_pack_words": lesson_pack_words,
        "cefr_level": cefr_level,
        "course_language": course_language,
        "speakers_langauge": speakers_langauge,

    }

    if current_basic_user == None:
        return HttpResponseRedirect("/auth/login/")
    else:
        return render(request, "basic_vocab_container/learning.html", data)
