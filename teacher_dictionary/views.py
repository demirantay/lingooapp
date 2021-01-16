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

from .models import TeacherDictionary, TeacherDictionaryWord


def teacher_dictionary_explore(request):
    """
    in this view the teachers can see the listings of all of the dictionaries
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

    # Get all of the dictionaries
    try:
        all_dictionaries = TeacherDictionary.objects.all()
    except ObjectDoesNotExist:
        all_dictionaries = None

    data = {
        "current_basic_user": current_basic_user,
        "current_basic_user_profile": current_basic_user_profile,
        "current_teacher_profile": current_teacher_profile,
        "all_dictionaries": all_dictionaries,
    }

    if "teacher_user_logged_in" in request.session:
        return render(request, "teacher_dictionary/explore.html", data)
    else:
        return HttpResponseRedirect("/")


def teacher_dictionary_build(request, dict_lang, dict_speaker_language):
    """
    in this page the teachers can see a specific dictionary and do CRUD
    opeartions on the dictioanry
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

    # Getting the current dictionary
    try:
        current_dictionary = TeacherDictionary.objects.get(
            dictionary_language=dict_lang,
            dictionary_speakers_language=dict_speaker_language,
        )
    except ObjectDoesNotExist:
        current_dictionary = None

    # Getting all the words of the current dictionary
    try:
        all_words = TeacherDictionaryWord.objects.filter(
            dictionary=current_dictionary
        ).order_by("-id")
    except ObjectDoesNotExist:
        all_words = None

    # Add a word to the dictioanry form processing
    empty_input = False

    if request.POST.get("teacher_dict_word_add_submit_btn"):
        word = request.POST.get("word")
        word_translation = request.POST.get("word_translation")
        # check if inputs are empty, if not then submit
        if bool(word) == False or word == "" or \
           bool(word_translation) == False or word_translation == "":
            empty_input = True
        else:
            new_word = TeacherDictionaryWord(
                user=current_basic_user,
                teacher=current_teacher_profile,
                dictionary=current_dictionary,
                word=word,
                translation=word_translation,
            )
            new_word.save()
            return HttpResponseRedirect(
                "/teacher/dictionary/build/" + dict_lang + "/"
                + dict_speaker_language + "/"
            )

    # Push to production automation (update or create/never nuke and re-create)

    data = {
        "current_basic_user": current_basic_user,
        "current_basic_user_profile": current_basic_user_profile,
        "current_teacher_profile": current_teacher_profile,
        "all_words": all_words,
        "dict_lang": dict_lang,
        "dict_speaker_language": dict_speaker_language,
        "empty_input": empty_input,
        "current_dictionary": current_dictionary,
    }

    if "teacher_user_logged_in" in request.session:
        return render(request, "teacher_dictionary/build.html", data)
    else:
        return HttpResponseRedirect("/")


def teacher_dictionary_update(request, id):
    """
    in this page the users can update the words of a dictionary
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

    # Get the current word
    try:
        current_word = TeacherDictionaryWord.objects.get(id=id)
    except ObjectDoesNotExist:
        current_word = None

    # Update the current word form processing
    empty_input = False

    if request.POST.get("update_teacher_dictionary_word_submit_btn"):
        new_word = request.POST.get("new_word")
        new_word_translation = request.POST.get("new_word_translation")
        # check if inputs are empty
        if bool(new_word) == False or new_word == "" or \
           bool(new_word_translation) == False or new_word_translation == "":
            empty_input = True
        else:
            current_word.word = new_word
            current_word.translation = new_word_translation
            current_word.save()
            return HttpResponseRedirect(
                "/teacher/dictionary/build/" + current_word.dictionary.dictionary_language
                + "/" + current_word.dictionary.dictionary_speakers_language + "/"
            )

    data = {
        "current_basic_user": current_basic_user,
        "current_basic_user_profile": current_basic_user_profile,
        "current_teacher_profile": current_teacher_profile,
        "current_word": current_word,
        "empty_input": empty_input,
    }

    if "teacher_user_logged_in" in request.session:
        return render(request, "teacher_dictionary/update.html", data)
    else:
        return HttpResponseRedirect("/")
