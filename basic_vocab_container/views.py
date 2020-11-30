# Main Imports
import json

# Django Imports
from django.shortcuts import render, get_object_or_404, HttpResponse
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.core.files import File
from django.contrib.auth.models import User
from django.utils import timezone

# My Module ImportsImports
from .models import BasicVocabularyContainer, StudentVocabProgress
from .models import BasicVocabErrorReport
from basic_language_explore.models import BasicLanguageCourse, Student, Language
from profile_settings.models import BasicUserProfile
from teacher_authentication.models import TeacherUserProfile
from profile_app.models import LessonTrackRecord

from utils.session_utils import get_current_user, get_current_user_profile
from utils.session_utils import get_current_teacher_user_profile
from utils.access_control import delete_teacher_user_session
from utils.update_levels import update_levels
from utils.update_track_record import update_track_record


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

    # Get the next 10 words to learn and display them to the user
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

    # if levels do not have the word limit that they should have return to home
    if cefr_level == "a0":
        if a0_words < 100:
            return HttpResponseRedirect("/")
    elif cefr_level == "a1":
        if a1_words < 500:
            return HttpResponseRedirect("/")
    elif cefr_level == "a2":
        if a2_words < 1000:
            return HttpResponseRedirect("/")
    elif cefr_level == "b1":
        if b1_words < 2000:
            return HttpResponseRedirect("/")
    elif cefr_level == "b2":
        if b2_words < 4000:
            return HttpResponseRedirect("/")
    elif cefr_level == "c1":
        if c1_words < 8000:
            return HttpResponseRedirect("/")
    elif cefr_level == "advanced":
        if advanced_words < 16000:
            return HttpResponseRedirect("/")

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

    # If previous level is not finished return home beacuse you cannot jump
    # between levels you need to finish one, in order to move to the next.
    a0_progress = 0
    a1_progress = 0
    a2_progress = 0
    b1_progress = 0
    b2_progress = 0
    c1_progress = 0
    advanced_progress = 0

    for word in current_student_progress:
        if word.vocab_container_word.level == "a0":
            if word.is_learned == True:
                a0_progress += 1
            else:
                continue
        elif word.vocab_container_word.level == "a1":
            if word.is_learned == True:
                a1_progress += 1
            else:
                continue
        elif word.vocab_container_word.level == "a2":
            if word.is_learned == True:
                a2_progress += 1
            else:
                continue
        elif word.vocab_container_word.level == "b1":
            if word.is_learned == True:
                b1_progress += 1
            else:
                continue
        elif word.vocab_container_word.level == "b2":
            if word.is_learned == True:
                b2_progress += 1
            else:
                continue
        elif word.vocab_container_word.level == "c1":
            if word.is_learned == True:
                c1_progress += 1
            else:
                continue
        elif word.vocab_container_word.level == "advanced":
            if word.is_learned == True:
                advanced_progress += 1
            else:
                continue

    a0_completed = False
    a1_completed = False
    a2_completed = False
    b1_completed = False
    b2_completed = False
    c1_completed = False
    advanced_completed = False

    # Im checking each one with their own if block because if you do all of
    # them in a single if block the first one a0_progress code block gets
    # executed and than stops because it found the neccessary conditional
    # which makes other progress bars not work

    if a0_progress >= 100:
        a0_completed = True

    if a1_progress >= 500:
        a1_completed = True

    if a2_progress >= 1000:
        a2_completed = True

    if b1_progress >= 2000:
        b1_completed = True

    if b2_progress >= 4000:
        b2_completed = True

    if c1_progress >= 8000:
        c1_completed = True

    if advanced_progress >= 16000:
        advanced_completed = True

    if cefr_level == "a0":
        pass
    elif cefr_level == "a1":
        if a0_completed == False:
            return HttpResponseRedirect("/")
    elif cefr_level == "a2":
        if a1_completed == False:
            return HttpResponseRedirect("/")
    elif cefr_level == "b1":
        if a2_completed == False:
            return HttpResponseRedirect("/")
    elif cefr_level == "b2":
        if b1_completed == False:
            return HttpResponseRedirect("/")
    elif cefr_level == "c1":
        if b2_completed == False:
            return HttpResponseRedirect("/")
    elif cefr_level == "advanced":
        if c1_completed == False:
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
        return render(request, "basic_vocab_container/learning_start_v2.html", data)


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

    # Get the next 10 words to learn and display them to the user
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

    # if levels do not have the word limit that they should have return to home
    if cefr_level == "a0":
        if a0_words < 100:
            return HttpResponseRedirect("/")
    elif cefr_level == "a1":
        if a1_words < 500:
            return HttpResponseRedirect("/")
    elif cefr_level == "a2":
        if a2_words < 1000:
            return HttpResponseRedirect("/")
    elif cefr_level == "b1":
        if b1_words < 2000:
            return HttpResponseRedirect("/")
    elif cefr_level == "b2":
        if b2_words < 4000:
            return HttpResponseRedirect("/")
    elif cefr_level == "c1":
        if c1_words < 8000:
            return HttpResponseRedirect("/")
    elif cefr_level == "advanced":
        if advanced_words < 16000:
            return HttpResponseRedirect("/")

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

    # Get the all of the learned words length
    all_learned_words_length = len(current_student_progress) - len(unlearned_words)

    # If the current lesson pack do not serve the lesson
    if len(unlearned_words) < 10:
        return HttpResponseRedirect("/")

    # If previous level is not finished return home beacuse you cannot jump
    # between levels you need to finish one, in order to move to the next.
    a0_progress = 0
    a1_progress = 0
    a2_progress = 0
    b1_progress = 0
    b2_progress = 0
    c1_progress = 0
    advanced_progress = 0

    for word in current_student_progress:
        if word.vocab_container_word.level == "a0":
            if word.is_learned == True:
                a0_progress += 1
            else:
                continue
        elif word.vocab_container_word.level == "a1":
            if word.is_learned == True:
                a1_progress += 1
            else:
                continue
        elif word.vocab_container_word.level == "a2":
            if word.is_learned == True:
                a2_progress += 1
            else:
                continue
        elif word.vocab_container_word.level == "b1":
            if word.is_learned == True:
                b1_progress += 1
            else:
                continue
        elif word.vocab_container_word.level == "b2":
            if word.is_learned == True:
                b2_progress += 1
            else:
                continue
        elif word.vocab_container_word.level == "c1":
            if word.is_learned == True:
                c1_progress += 1
            else:
                continue
        elif word.vocab_container_word.level == "advanced":
            if word.is_learned == True:
                advanced_progress += 1
            else:
                continue

    a0_completed = False
    a1_completed = False
    a2_completed = False
    b1_completed = False
    b2_completed = False
    c1_completed = False
    advanced_completed = False

    # Im checking each one with their own if block because if you do all of
    # them in a single if block the first one a0_progress code block gets
    # executed and than stops because it found the neccessary conditional
    # which makes other progress bars not work

    if a0_progress >= 100:
        a0_completed = True

    if a1_progress >= 500:
        a1_completed = True

    if a2_progress >= 1000:
        a2_completed = True

    if b1_progress >= 2000:
        b1_completed = True

    if b2_progress >= 4000:
        b2_completed = True

    if c1_progress >= 8000:
        c1_completed = True

    if advanced_progress >= 16000:
        advanced_completed = True

    if cefr_level == "a0":
        pass
    elif cefr_level == "a1":
        if a0_completed == False:
            return HttpResponseRedirect("/")
    elif cefr_level == "a2":
        if a1_completed == False:
            return HttpResponseRedirect("/")
    elif cefr_level == "b1":
        if a2_completed == False:
            return HttpResponseRedirect("/")
    elif cefr_level == "b2":
        if b1_completed == False:
            return HttpResponseRedirect("/")
    elif cefr_level == "c1":
        if b2_completed == False:
            return HttpResponseRedirect("/")
    elif cefr_level == "advanced":
        if c1_completed == False:
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

        # and add +10 xp and update levels
        current_student.xp += 10
        update_levels(current_student)
        current_student.save()

        # Update track record
        try:
            current_record = LessonTrackRecord.objects.get(
                creation_date=timezone.now(),
                user=current_basic_user_profile
            )
        except ObjectDoesNotExist:
            current_record = None

        update_track_record(current_record, LessonTrackRecord, current_basic_user_profile)

        return HttpResponseRedirect("/")

    data = {
        "current_basic_user": current_basic_user,
        "current_basic_user_profile": current_basic_user_profile,
        "lesson_pack": lesson_pack,
        "lesson_pack_words": lesson_pack_words,
        "cefr_level": cefr_level,
        "course_language": course_language,
        "speakers_langauge": speakers_langauge,
        "current_student": current_student,
        "current_course": current_course,
        "all_learned_words_length": all_learned_words_length,
    }

    if current_basic_user == None:
        return HttpResponseRedirect("/auth/login/")
    else:
        return render(request, "basic_vocab_container/learning.html", data)


def basic_vocab_review(request, course_language, speakers_langauge):
    """
    in this view the users can review the languages that they have learned in
    their student progresses for each courses
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

    # Get the current students progress words for is_learned words
    try:
        current_student_progress = StudentVocabProgress.objects.filter(
            student=current_student,
            is_learned=True
        )
    except ObjectDoesNotExist:
        current_student_progress = None

    # Get the current lessons packs (25) words
    unreviewed_words = []

    for word in current_student_progress:
        if word.is_reviewed == False:
            unreviewed_words.append(word)

    lesson_pack = []
    current_lesson_length = 0
    review_pack_words = {}

    def get_review_pack_words(limit):
        for word in unreviewed_words[:limit]:
            review_pack_words[word.vocab_container_word.word] = word.vocab_container_word.word_translation

    if len(unreviewed_words) >= 25:
        lesson_pack = unreviewed_words[:25]
        get_review_pack_words(25)
        current_lesson_length = 25
    elif len(unreviewed_words) < 25 and len(unreviewed_words) >= 20:
        lesson_pack = unreviewed_words[:20]
        get_review_pack_words(20)
        current_lesson_length = 20
    elif len(unreviewed_words) < 20 and len(unreviewed_words) >= 15:
        lesson_pack = unreviewed_words[:15]
        get_review_pack_words(15)
        current_lesson_length = 15
    elif len(unreviewed_words) < 15 and len(unreviewed_words) >= 10:
        lesson_pack = unreviewed_words[:10]
        get_review_pack_words(10)
        current_lesson_length = 10
    elif len(unreviewed_words) < 10 and len(unreviewed_words) >= 5:
        lesson_pack = unreviewed_words[:5]
        get_review_pack_words(5)
        current_lesson_length = 5
    elif len(unreviewed_words) < 5:
        # If the current needs_reviewing words are less than 5 then set all of
        # the words needs_reviewing to false, so that user can review new cycle
        for word in current_student_progress:
            word.is_reviewed = False
            word.save()
        return HttpResponseRedirect("/")
    else:
        pass

    # If everything is done and the lesson is learned correctly then update
    # the is_reviewed boolean columns of the progress words
    if request.POST.get("vocab_review_lesson_finish_button"):
        hidden_errors_array = request.POST.get("hidden_errors_array")

        parsed_json = []
        if hidden_errors_array:
            parsed_json = json.loads(hidden_errors_array)
        else:
            parsed_json = []

        # print(current_lesson_length)

        # Add the ERRORs
        if bool(parsed_json) == False or parsed_json == {} or parsed_json == []:
            # its empty pass
            pass
        else:
            # Get the current vocab container recrod
            for data in parsed_json:
                for word in lesson_pack:
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

        # Make the words reviewed = true
        for word in lesson_pack:
            word.is_reviewed = True
            word.save()

        # and add +10 xp and update levels
        current_student.xp += 10

        update_levels(current_student)

        current_student.save()

        # Update track record
        try:
            current_record = LessonTrackRecord.objects.get(
                creation_date=timezone.now(),
                user=current_basic_user_profile
            )
        except ObjectDoesNotExist:
            current_record = None

        update_track_record(current_record, LessonTrackRecord, current_basic_user_profile)

        return HttpResponseRedirect("/")

    data = {
        "current_basic_user": current_basic_user,
        "current_basic_user_profile": current_basic_user_profile,
        "lesson_pack": lesson_pack,
        "review_pack_words": review_pack_words,
        "course_language": course_language,
        "speakers_langauge": speakers_langauge,
        "current_lesson_length": current_lesson_length,
        "current_student": current_student,
        "current_course": current_course,
        "all_learned_words_length": len(current_student_progress),
    }

    if current_basic_user == None:
        return HttpResponseRedirect("/auth/login/")
    else:
        return render(request, "basic_vocab_container/review.html", data)
