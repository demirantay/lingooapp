# Main Imports
import json
import datetime

# Django Imports
from django.shortcuts import render, get_object_or_404, HttpResponse
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.core.files import File
from django.contrib.auth.models import User
from django.utils import timezone

# My Module ImportsImports
from .models import Bill, LastBillCreationDate
from profile_settings.models import BasicUserProfile
from teacher_authentication.models import TeacherUserProfile
from utils.session_utils import get_current_user, get_current_user_profile
from utils.session_utils import get_current_teacher_user_profile
from utils.access_control import delete_teacher_user_session


def basic_create_bill(request):
    """
    in this view the user can create a new bill for other users to vote on
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

    # creating a new bill form process
    empty_input = False
    already_created_one_today = False

    if request.POST.get("basic_bill_create_submit_button"):
        title = request.POST.get("title")
        category = request.POST.get("category")
        content = request.POST.get("bill_content")

        # check if the inputs are empty
        if bool(title) == False or title == "" or \
           bool(category) == False or category == "" or \
           bool(content) == False or content == "":
            empty_input = True
        else:
            # check if the user has created a bill today, you can only create
            #  one bill in a single day. To prevent spamming and brute forcing.
            try:
                last_creation_date = LastBillCreationDate.objects.get(
                    user_profile=current_basic_user_profile
                )
            except ObjectDoesNotExist:
                last_creation_date = None

            if last_creation_date == None:
                # if the last creation date does not exists create the new bill
                # and create a new bill
                new_creation_date = LastBillCreationDate(
                    user_profile=current_basic_user_profile
                )
                new_creation_date.save()
                new_bill = Bill(
                    sponsor=current_basic_user_profile,
                    title=title,
                    content=content,
                    status="voting",
                    category=category,
                )
                new_bill.save()
                return HttpResponseRedirect(
                    "/voting/congress/bill/read/" + str(new_bill.id) + "/"
                )

            # check if theere is alredy created bill today
            if str(last_creation_date.creation_date) == str(timezone.now().date()):
                already_created_one_today = True
            else:
                # if no then go ahead and create one
                #  and update latest creation date
                last_creation_date.creation_date = timezone.now()
                last_creation_date.save()

                new_bill = Bill(
                    sponsor=current_basic_user_profile,
                    title=title,
                    content=content,
                    status="voting",
                    category=category,
                )
                new_bill.save()
                return HttpResponseRedirect(
                    "/voting/congress/bill/read/" + str(new_bill.id) + "/"
                )


    data = {
        "current_basic_user": current_basic_user,
        "current_basic_user_profile": current_basic_user_profile,
        "current_teacher_profile": current_teacher_profile,
        "empty_input": empty_input,
        "already_created_one_today": already_created_one_today,
    }

    if current_basic_user == None:
        return HttpResponseRedirect("/auth/login/")
    else:
        return render(request, "basic_voting_sys/create_bill.html", data)


def basic_read_bill(request, bill_id):
    """
    in this view the user can view a specific bill and what it is about.
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

    # Getting the current bill
    try:
        current_bill = Bill.objects.get(id=bill_id)
    except ObjectDoesNotExist:
        current_bill = None

    # Getting the current history

    # Getting the votes

    # Vote form processing

    # Delete request form processing

    data = {
        "current_basic_user": current_basic_user,
        "current_basic_user_profile": current_basic_user_profile,
        "current_teacher_profile": current_teacher_profile,
        "current_bill": current_bill,
    }

    if current_basic_user == None:
        return HttpResponseRedirect("/auth/login/")
    else:
        return render(request, "basic_voting_sys/read_bill.html", data)


def basic_update_bill(request, bill_id):
    """

    """

    data = {

    }

    return render(request, "basic_voting_sys/update_bill.html", data)


def basic_bill_landing_page(request):
    """
    """

    data = {

    }

    return render(request, "basic_voting_sys/landing_page.html", data)


def basic_bill_passed_page(request):
    """
    """

    data = {

    }

    return render(request, "basic_voting_sys/passed_page.html", data)


def basic_bill_shelved_page(request):
    """
    """

    data = {

    }

    return render(request, "basic_voting_sys/shelved_page.html", data)


def basic_bill_new_page(request):
    """
    """

    data = {

    }

    return render(request, "basic_voting_sys/new_page.html", data)
