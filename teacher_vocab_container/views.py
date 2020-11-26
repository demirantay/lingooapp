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
from .models import TeacherVocabularyContainer
from basic_vocab_container.models import BasicVocabularyContainer
from basic_language_explore.models import BasicLanguageCourse

from utils.session_utils import get_current_user, get_current_user_profile
from utils.session_utils import get_current_teacher_user_profile


def teacher_vocab_container_overview(request):
    """
    in this view the teachers can create the vocabulary packs
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

    # Listing all of the words in tables
    # A0
    try:
        a0_word_list = TeacherVocabularyContainer.objects.filter(
            course=current_teacher_profile.teacher_course, level="a0"
        ).order_by("id")
    except ObjectDoesNotExist:
        a0_word_list = None

    # A0 words id count such as 1, 2, 3, 4 ... 100 .. etc.
    a0_word_count = {}
    count = 0
    for word in a0_word_list:
        count += 1
        a0_word_count[word.id] = count

    # A1
    try:
        a1_word_list = TeacherVocabularyContainer.objects.filter(
            course=current_teacher_profile.teacher_course, level="a1"
        ).order_by("id")
    except ObjectDoesNotExist:
        a1_word_list = None

    # A1 words id count such as 1, 2, 3, 4 ... 100 .. etc.
    a1_word_count = {}
    count = 0
    for word in a1_word_list:
        count += 1
        a1_word_count[word.id] = count

    # A2
    try:
        a2_word_list = TeacherVocabularyContainer.objects.filter(
            course=current_teacher_profile.teacher_course, level="a2"
        ).order_by("id")
    except ObjectDoesNotExist:
        a2_word_list = None

    # A1 words id count such as 1, 2, 3, 4 ... 100 .. etc.
    a2_word_count = {}
    count = 0
    for word in a2_word_list:
        count += 1
        a2_word_count[word.id] = count

    # B1
    try:
        b1_word_list = TeacherVocabularyContainer.objects.filter(
            course=current_teacher_profile.teacher_course, level="b1"
        ).order_by("id")
    except ObjectDoesNotExist:
        b1_word_list = None

    # A1 words id count such as 1, 2, 3, 4 ... 100 .. etc.
    b1_word_count = {}
    count = 0
    for word in b1_word_list:
        count += 1
        b1_word_count[word.id] = count

    # B2
    try:
        b2_word_list = TeacherVocabularyContainer.objects.filter(
            course=current_teacher_profile.teacher_course, level="b2"
        ).order_by("id")
    except ObjectDoesNotExist:
        b2_word_list = None

    b2_word_count = {}
    count = 0
    for word in b2_word_list:
        count += 1
        b2_word_count[word.id] = count

    # C1
    try:
        c1_word_list = TeacherVocabularyContainer.objects.filter(
            course=current_teacher_profile.teacher_course, level="c1"
        ).order_by("id")
    except ObjectDoesNotExist:
        c1_word_list = None

    c1_word_count = {}
    count = 0
    for word in c1_word_list:
        count += 1
        c1_word_count[word.id] = count

    # Advanced
    try:
        advanced_word_list = TeacherVocabularyContainer.objects.filter(
            course=current_teacher_profile.teacher_course, level="advanced"
        ).order_by("id")
    except ObjectDoesNotExist:
        advanced_word_list = None

    advanced_word_count = {}
    count = 0
    for word in advanced_word_list:
        count += 1
        advanced_word_count[word.id] = count

    # vocab add A0 processing
    a0_limit_reached = False
    empty_a0_input = False

    if request.POST.get("teacher_word_add_a0_submit"):
        word = request.POST.get("word")
        translation = request.POST.get("translation")

        # check if a0 list has 100 words
        if len(a0_word_list) > 100:
            a0_limit_reached = True
        else:
            # check if inputs are empty
            if bool(word) == False or word == "" or \
               bool(translation) == False or translation == "":
                empty_a0_input = True
            else:
                new_word_record = TeacherVocabularyContainer(
                    course=current_teacher_profile.teacher_course,
                    teacher=current_teacher_profile,
                    word=word,
                    word_translation=translation,
                    level="a0"
                )
                new_word_record.save()
                return HttpResponseRedirect("/teacher/vocab/container/overview/")

    # vocab add A1 processing
    a1_limit_reached = False
    empty_a1_input = False

    if request.POST.get("teacher_word_add_a1_submit"):
        word = request.POST.get("word")
        translation = request.POST.get("translation")

        # check if a1 list has 500 words
        if len(a1_word_list) > 500:
            a1_limit_reached = True
        else:
            # check if it is empty
            if bool(word) == False or word == "" or \
               bool(translation) == False or translation == "":
                empty_a0_input = True
            else:
                new_word_record = TeacherVocabularyContainer(
                    course=current_teacher_profile.teacher_course,
                    teacher=current_teacher_profile,
                    word=word,
                    word_translation=translation,
                    level="a1"
                )
                new_word_record.save()
                return HttpResponseRedirect("/teacher/vocab/container/overview/")

    # vocab add A2 processing
    a2_limit_reached = False
    empty_a2_input = False

    if request.POST.get("teacher_word_add_a2_submit"):
        word = request.POST.get("word")
        translation = request.POST.get("translation")

        # check if a2 list has 1000 words
        if len(a2_word_list) > 1000:
            a2_limit_reached = True
        else:
            # check if it is empty
            if bool(word) == False or word == "" or \
               bool(translation) == False or translation == "":
                empty_a2_input = True
            else:
                new_word_record = TeacherVocabularyContainer(
                    course=current_teacher_profile.teacher_course,
                    teacher=current_teacher_profile,
                    word=word,
                    word_translation=translation,
                    level="a2"
                )
                new_word_record.save()
                return HttpResponseRedirect("/teacher/vocab/container/overview/")

    # vocab add B1 processing
    b1_limit_reached = False
    empty_b1_input = False

    if request.POST.get("teacher_word_add_b1_submit"):
        word = request.POST.get("word")
        translation = request.POST.get("translation")

        # check if b1 list has 2000 words
        if len(b1_word_list) > 2000:
            b1_limit_reached = True
        else:
            # check if it is empty
            if bool(word) == False or word == "" or \
               bool(translation) == False or translation == "":
                empty_b1_input = True
            else:
                new_word_record = TeacherVocabularyContainer(
                    course=current_teacher_profile.teacher_course,
                    teacher=current_teacher_profile,
                    word=word,
                    word_translation=translation,
                    level="b1"
                )
                new_word_record.save()
                return HttpResponseRedirect("/teacher/vocab/container/overview/")

    # vocab add B2 processing
    b2_limit_reached = False
    empty_b2_input = False

    if request.POST.get("teacher_word_add_b2_submit"):
        word = request.POST.get("word")
        translation = request.POST.get("translation")

        # check if b2 list has 4000 words
        if len(b2_word_list) > 4000:
            b2_limit_reached = True
        else:
            # check if it is empty
            if bool(word) == False or word == "" or \
               bool(translation) == False or translation == "":
                empty_b2_input = True
            else:
                new_word_record = TeacherVocabularyContainer(
                    course=current_teacher_profile.teacher_course,
                    teacher=current_teacher_profile,
                    word=word,
                    word_translation=translation,
                    level="b2"
                )
                new_word_record.save()
                return HttpResponseRedirect("/teacher/vocab/container/overview/")

    # vocab add C1 processing
    c1_limit_reached = False
    empty_c1_input = False

    if request.POST.get("teacher_word_add_c1_submit"):
        word = request.POST.get("word")
        translation = request.POST.get("translation")

        # check if c1 list has 8000 words
        if len(c1_word_list) > 8000:
            c1_limit_reached = True
        else:
            # check if it is empty
            if bool(word) == False or word == "" or \
               bool(translation) == False or translation == "":
                empty_c1_input = True
            else:
                new_word_record = TeacherVocabularyContainer(
                    course=current_teacher_profile.teacher_course,
                    teacher=current_teacher_profile,
                    word=word,
                    word_translation=translation,
                    level="c1"
                )
                new_word_record.save()
                return HttpResponseRedirect("/teacher/vocab/container/overview/")

    # vocab add Advanced processing
    advanced_limit_reached = False
    empty_advanced_input = False

    if request.POST.get("teacher_word_add_advanced_submit"):
        word = request.POST.get("word")
        translation = request.POST.get("translation")

        # check if advanced list has 16000 words
        if len(c1_word_list) > 16000:
            advanced_limit_reached = True
        else:
            # check if it is empty
            if bool(word) == False or word == "" or \
               bool(translation) == False or translation == "":
                empty_advanced_input = True
            else:
                new_word_record = TeacherVocabularyContainer(
                    course=current_teacher_profile.teacher_course,
                    teacher=current_teacher_profile,
                    word=word,
                    word_translation=translation,
                    level="advanced"
                )
                new_word_record.save()
                return HttpResponseRedirect("/teacher/vocab/container/overview/")

    # VOCAB SHORT CUT FORM PROCESSINGS

    # Shortcut - A0
    hidden_a0_limit_reached = False
    hidden_empty_a0_input = False

    if request.POST.get("teacher_vocab_shortcut_a0_submit_btn"):
        new_word = request.POST.get("new_word")
        new_word_translation = request.POST.get("new_word_translation")

        if len(a0_word_list) >= 100:
            hidden_a0_limit_reached = True
        else:
            # check if it is empty
            if bool(new_word) == False or new_word == "" or \
               bool(new_word_translation) == False or new_word_translation == "":
                hidden_empty_a0_input = True
            else:
                new_word_record = TeacherVocabularyContainer(
                    course=current_teacher_profile.teacher_course,
                    teacher=current_teacher_profile,
                    word=new_word,
                    word_translation=new_word_translation,
                    level="a0"
                )
                new_word_record.save()
                return HttpResponseRedirect("/teacher/vocab/container/overview/")

    # Shortcut - A1
    hidden_a1_limit_reached = False
    hidden_empty_a1_input = False

    if request.POST.get("teacher_vocab_shortcut_a1_submit_btn"):
        new_word = request.POST.get("new_word")
        new_word_translation = request.POST.get("new_word_translation")

        if len(a1_word_list) >= 500:
            hidden_a1_limit_reached = True
        else:
            # check if it is empty
            if bool(new_word) == False or new_word == "" or \
               bool(new_word_translation) == False or new_word_translation == "":
                hidden_empty_a1_input = True
            else:
                new_word_record = TeacherVocabularyContainer(
                    course=current_teacher_profile.teacher_course,
                    teacher=current_teacher_profile,
                    word=new_word,
                    word_translation=new_word_translation,
                    level="a1"
                )
                new_word_record.save()
                return HttpResponseRedirect("/teacher/vocab/container/overview/")

    # Shortcut - A2
    hidden_a2_limit_reached = False
    hidden_empty_a2_input = False

    if request.POST.get("teacher_vocab_shortcut_a2_submit_btn"):
        new_word = request.POST.get("new_word")
        new_word_translation = request.POST.get("new_word_translation")

        if len(a2_word_list) >= 1000:
            hidden_a2_limit_reached = True
        else:
            # check if it is empty
            if bool(new_word) == False or new_word == "" or \
               bool(new_word_translation) == False or new_word_translation == "":
                hidden_empty_a2_input = True
            else:
                new_word_record = TeacherVocabularyContainer(
                    course=current_teacher_profile.teacher_course,
                    teacher=current_teacher_profile,
                    word=new_word,
                    word_translation=new_word_translation,
                    level="a2"
                )
                new_word_record.save()
                return HttpResponseRedirect("/teacher/vocab/container/overview/")

    # Shortcut - B1
    hidden_b1_limit_reached = False
    hidden_empty_b1_input = False

    if request.POST.get("teacher_vocab_shortcut_b1_submit_btn"):
        new_word = request.POST.get("new_word")
        new_word_translation = request.POST.get("new_word_translation")

        if len(b1_word_list) >= 2000:
            hidden_b1_limit_reached = True
        else:
            # check if it is empty
            if bool(new_word) == False or new_word == "" or \
               bool(new_word_translation) == False or new_word_translation == "":
                hidden_empty_b1_input = True
            else:
                new_word_record = TeacherVocabularyContainer(
                    course=current_teacher_profile.teacher_course,
                    teacher=current_teacher_profile,
                    word=new_word,
                    word_translation=new_word_translation,
                    level="b1"
                )
                new_word_record.save()
                return HttpResponseRedirect("/teacher/vocab/container/overview/")

    # Shortcut - B2
    hidden_b2_limit_reached = False
    hidden_empty_b2_input = False

    if request.POST.get("teacher_vocab_shortcut_b2_submit_btn"):
        new_word = request.POST.get("new_word")
        new_word_translation = request.POST.get("new_word_translation")

        if len(b2_word_list) >= 4000:
            hidden_b2_limit_reached = True
        else:
            # check if it is empty
            if bool(new_word) == False or new_word == "" or \
               bool(new_word_translation) == False or new_word_translation == "":
                hidden_empty_b2_input = True
            else:
                new_word_record = TeacherVocabularyContainer(
                    course=current_teacher_profile.teacher_course,
                    teacher=current_teacher_profile,
                    word=new_word,
                    word_translation=new_word_translation,
                    level="b2"
                )
                new_word_record.save()
                return HttpResponseRedirect("/teacher/vocab/container/overview/")

    # Shortcut - C1
    hidden_c1_limit_reached = False
    hidden_empty_c1_input = False

    if request.POST.get("teacher_vocab_shortcut_c1_submit_btn"):
        new_word = request.POST.get("new_word")
        new_word_translation = request.POST.get("new_word_translation")

        if len(b2_word_list) >= 8000:
            hidden_c1_limit_reached = True
        else:
            # check if it is empty
            if bool(new_word) == False or new_word == "" or \
               bool(new_word_translation) == False or new_word_translation == "":
                hidden_empty_c1_input = True
            else:
                new_word_record = TeacherVocabularyContainer(
                    course=current_teacher_profile.teacher_course,
                    teacher=current_teacher_profile,
                    word=new_word,
                    word_translation=new_word_translation,
                    level="c1"
                )
                new_word_record.save()
                return HttpResponseRedirect("/teacher/vocab/container/overview/")

    # Shortcut - Advanced
    hidden_advanced_limit_reached = False
    hidden_empty_advanced_input = False

    if request.POST.get("teacher_vocab_shortcut_advanced_submit_btn"):
        new_word = request.POST.get("new_word")
        new_word_translation = request.POST.get("new_word_translation")

        if len(b2_word_list) >= 16000:
            hidden_advanced_limit_reached = True
        else:
            # check if it is empty
            if bool(new_word) == False or new_word == "" or \
               bool(new_word_translation) == False or new_word_translation == "":
                hidden_empty_advanced_input = True
            else:
                new_word_record = TeacherVocabularyContainer(
                    course=current_teacher_profile.teacher_course,
                    teacher=current_teacher_profile,
                    word=new_word,
                    word_translation=new_word_translation,
                    level="advanced"
                )
                new_word_record.save()
                return HttpResponseRedirect("/teacher/vocab/container/overview/")

    # Push to Production Form Processing
    production_push_error = False
    production_push_success = False

    try:
        prod_course = BasicLanguageCourse.objects.get(
            course_language=current_teacher_profile.teacher_course.course_language,
            course_speakers_language=current_teacher_profile.teacher_course.course_speakers_language
        )
    except ObjectDoesNotExist:
        prod_course = None

    # A0 Form
    if request.POST.get("teacher_vocab_container_push_production_a0_submit"):
        # check if the list is at 100
        if len(a0_word_list) == 100:
            # get the current production course and it's words list
            try:
                prod_a0_words = BasicVocabularyContainer.objects.filter(
                    course=prod_course,
                    level="a0"
                )
            except ObjectDoesNotExist:
                prod_a0_words = None

            # delete all of the a0 words in the production
            prod_a0_words.delete()

            # update all of the new a0 words in the production
            # with the current list
            for word in a0_word_list:
                new_prod_word = BasicVocabularyContainer(
                    course=prod_course,
                    word=word.word,
                    word_translation=word.word_translation,
                    level="a0"
                )
                new_prod_word.save()
                production_push_success = True
        else:
            production_push_error = True

    # A1 Push to Production Form Processing
    if request.POST.get("teacher_vocab_container_push_production_a1_submit"):
        # check if the list is at 500
        if len(a1_word_list) == 500:
            # get the current production course and it's words list
            try:
                prod_a1_words = BasicVocabularyContainer.objects.filter(
                    course=prod_course,
                    level="a1"
                )
            except ObjectDoesNotExist:
                prod_a1_words = None

            # delete all of the a0 words in the production
            prod_a1_words.delete()

            # update all of the new a0 words in the production
            # with the current list
            for word in a1_word_list:
                new_prod_word = BasicVocabularyContainer(
                    course=prod_course,
                    word=word.word,
                    word_translation=word.word_translation,
                    level="a1"
                )
                new_prod_word.save()
                production_push_success = True
        else:
            production_push_error = True

    # A2 Push to Production Form Processing
    if request.POST.get("teacher_vocab_container_push_production_a2_submit"):
        # check if the list is at 1000
        if len(a2_word_list) == 1000:
            # get the current production course and it's words list
            try:
                prod_a2_words = BasicVocabularyContainer.objects.filter(
                    course=prod_course,
                    level="a2"
                )
            except ObjectDoesNotExist:
                prod_a2_words = None

            # delete all of the a0 words in the production
            prod_a2_words.delete()

            # update all of the new a0 words in the production
            # with the current list
            for word in a2_word_list:
                new_prod_word = BasicVocabularyContainer(
                    course=prod_course,
                    word=word.word,
                    word_translation=word.word_translation,
                    level="a2"
                )
                new_prod_word.save()
                production_push_success = True
        else:
            production_push_error = True

    # B1 Push to Production Form Processing
    if request.POST.get("teacher_vocab_container_push_production_b1_submit"):
        # check if the list is at 2000
        if len(b1_word_list) == 2000:
            # get the current production course and it's words list
            try:
                prod_b1_words = BasicVocabularyContainer.objects.filter(
                    course=prod_course,
                    level="b1"
                )
            except ObjectDoesNotExist:
                prod_b1_words = None

            # delete all of the a0 words in the production
            prod_b1_words.delete()

            # update all of the new a0 words in the production
            # with the current list
            for word in b1_word_list:
                new_prod_word = BasicVocabularyContainer(
                    course=prod_course,
                    word=word.word,
                    word_translation=word.word_translation,
                    level="b1"
                )
                new_prod_word.save()
                production_push_success = True
        else:
            production_push_error = True

    # B2 Push to Production Form Processing
    if request.POST.get("teacher_vocab_container_push_production_b2_submit"):
        # check if the list is at 4000
        if len(b2_word_list) == 4000:
            # get the current production course and it's words list
            try:
                prod_b2_words = BasicVocabularyContainer.objects.filter(
                    course=prod_course,
                    level="b2"
                )
            except ObjectDoesNotExist:
                prod_b2_words = None

            # delete all of the a0 words in the production
            prod_b2_words.delete()

            # update all of the new a0 words in the production
            # with the current list
            for word in b2_word_list:
                new_prod_word = BasicVocabularyContainer(
                    course=prod_course,
                    word=word.word,
                    word_translation=word.word_translation,
                    level="b2"
                )
                new_prod_word.save()
                production_push_success = True
        else:
            production_push_error = True

    # C1 Push to Production Form Processing
    if request.POST.get("teacher_vocab_container_push_production_c1_submit"):
        # check if the list is at 8000
        if len(c1_word_list) == 8000:
            # get the current production course and it's words list
            try:
                prod_c1_words = BasicVocabularyContainer.objects.filter(
                    course=prod_course,
                    level="c1"
                )
            except ObjectDoesNotExist:
                prod_c1_words = None

            # delete all of the c1 words in the production
            prod_c1_words.delete()

            # update all of the new c1 words in the production
            # with the current list
            for word in c1_word_list:
                new_prod_word = BasicVocabularyContainer(
                    course=prod_course,
                    word=word.word,
                    word_translation=word.word_translation,
                    level="c1"
                )
                new_prod_word.save()
                production_push_success = True
        else:
            production_push_error = True

    # Advanced Push to Production Form Processing
    if request.POST.get("teacher_vocab_container_push_production_advanced_submit"):
        # check if the list is at 16000
        if len(advanced_word_list) == 16000:
            # get the current production course and it's words list
            try:
                prod_advanced_words = BasicVocabularyContainer.objects.filter(
                    course=prod_course,
                    level="advanced"
                )
            except ObjectDoesNotExist:
                prod_advanced_words = None

            # delete all of the c1 words in the production
            prod_advanced_words.delete()

            # update all of the new c1 words in the production
            # with the current list
            for word in advanced_word_list:
                new_prod_word = BasicVocabularyContainer(
                    course=prod_course,
                    word=word.word,
                    word_translation=word.word_translation,
                    level="advanced"
                )
                new_prod_word.save()
                production_push_success = True
        else:
            production_push_error = True

    data = {
        "current_basic_user": current_basic_user,
        "current_basic_user_profile": current_basic_user_profile,
        "current_teacher_profile": current_teacher_profile,
        "a0_word_list": a0_word_list,
        "a0_word_count": a0_word_count,
        "a1_word_list": a1_word_list,
        "a1_word_count": a1_word_count,
        "a2_word_list": a2_word_list,
        "a2_word_count": a2_word_count,
        "b1_word_list": b1_word_list,
        "b1_word_count": b1_word_count,
        "b2_word_list": b2_word_list,
        "b2_word_count": b2_word_count,
        "c1_word_list": c1_word_list,
        "c1_word_count": c1_word_count,
        "advanced_word_list": advanced_word_list,
        "advanced_word_count": advanced_word_count,
        "a0_limit_reached": a0_limit_reached,
        "a1_limit_reached": a1_limit_reached,
        "a2_limit_reached": a2_limit_reached,
        "b1_limit_reached": b1_limit_reached,
        "b2_limit_reached": b2_limit_reached,
        "c1_limit_reached": c1_limit_reached,
        "advanced_limit_reached": advanced_limit_reached,
        "empty_a0_input": empty_a0_input,
        "empty_a1_input": empty_a1_input,
        "empty_a2_input": empty_a2_input,
        "empty_b1_input": empty_b1_input,
        "empty_b2_input": empty_b2_input,
        "empty_c1_input": empty_c1_input,
        "empty_advanced_input": empty_advanced_input,
        "hidden_a0_limit_reached": hidden_a0_limit_reached,
        "hidden_empty_a0_input": hidden_empty_a0_input,
        "hidden_a1_limit_reached": hidden_a1_limit_reached,
        "hidden_empty_a1_input": hidden_empty_a1_input,
        "hidden_a2_limit_reached": hidden_a2_limit_reached,
        "hidden_empty_a2_input": hidden_empty_a2_input,
        "hidden_b1_limit_reached": hidden_b1_limit_reached,
        "hidden_empty_b1_input": hidden_empty_b1_input,
        "hidden_b2_limit_reached": hidden_b2_limit_reached,
        "hidden_empty_b2_input": hidden_empty_b2_input,
        "hidden_c1_limit_reached": hidden_c1_limit_reached,
        "hidden_empty_c1_input": hidden_empty_c1_input,
        "hidden_advanced_limit_reached": hidden_advanced_limit_reached,
        "hidden_empty_advanced_input": hidden_empty_advanced_input,
        "production_push_error": production_push_error,
        "production_push_success": production_push_success,
    }

    if "teacher_user_logged_in" in request.session:
        return render(request, "teacher_vocab_container/overview_v2.html", data)
    else:
        return HttpResponseRedirect("/")


def teacher_vocab_container_edit(request, word_id, word):
    """
    in this view the teacher can add a word to the list
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

    # Get the current word record
    try:
        current_word = TeacherVocabularyContainer.objects.get(id=word_id)
    except ObjectDoesNotExist:
        current_word = None

    # edit form processing
    invalid_input = False
    empty_input = False

    if request.POST.get("teacher_vocab_container_edit_submit_btn"):
        updated_word = request.POST.get("updated_word")
        updated_translation = request.POST.get("updated_translation")

        # check if the words course is the same as the teachers one and see
        # if she is allowed update it
        if current_word.course == current_teacher_profile.teacher_course:
            # check if the input is empty
            if bool(updated_word) == False or updated_word == "" \
               or bool(updated_translation) == False or updated_translation == "":
                empty_input = True
            else:
                current_word.word = updated_word
                current_word.word_translation = updated_translation
                current_word.save()
                return HttpResponseRedirect("/teacher/vocab/container/overview/")
        else:
            invalid_input = True

    data = {
        "current_basic_user": current_basic_user,
        "current_basic_user_profile": current_basic_user_profile,
        "current_teacher_profile": current_teacher_profile,
        "current_word": current_word,
        "invalid_input": invalid_input,
        "empty_input": empty_input,
    }

    if "teacher_user_logged_in" in request.session:
        return render(request, "teacher_vocab_container/edit_word.html", data)
    else:
        return HttpResponseRedirect("/")


def teacher_vocab_container_add_sound(request, word_id):
    """
    in this view the teacher can add a word to the list
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

    # Get the current word record
    try:
        current_word = TeacherVocabularyContainer.objects.get(id=word_id)
    except ObjectDoesNotExist:
        current_word = None

    # Upload Audio form processing
    empty_input = False

    if request.POST.get("teacher_vocab_sound_submit_btn"):
        word_sound = request.FILES.get("word_sound")

        if bool(word_sound) == False:
            empty_input = True
        else:
            current_word.audio = word_sound
            current_word.save()
            return HttpResponseRedirect(
                "/vocab/container/sound/" + current_word.id + "/"
            )

    data = {
        "current_basic_user": current_basic_user,
        "current_basic_user_profile": current_basic_user_profile,
        "current_teacher_profile": current_teacher_profile,
        "current_word": current_word,
        "empty_input": empty_input,
    }

    if "teacher_user_logged_in" in request.session:
        return render(request, "teacher_vocab_container/add_sound.html", data)
    else:
        return HttpResponseRedirect("/")
