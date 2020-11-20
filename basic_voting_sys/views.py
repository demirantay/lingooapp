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
from .models import Bill, LastBillCreationDate, BillVote, BillUpdateHistory
from .models import BillDeleteRequest
from profile_settings.models import BasicUserProfile
from teacher_authentication.models import TeacherUserProfile
from basic_notifications.models import NotificationBase

from utils.session_utils import get_current_user, get_current_user_profile
from utils.session_utils import get_current_teacher_user_profile
from utils.access_control import delete_teacher_user_session

from algorithms.merge_sort import merge_sort


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
    try:
        current_bill_history = BillUpdateHistory.objects.filter(
            bill=current_bill
        ).order_by("-id")
    except ObjectDoesNotExist:
        current_bill_history = None

    current_bill_history_empty = False
    if bool(current_bill_history) == False or current_bill_history == []:
        current_bill_history_empty = True

    # Getting the votes
    try:
        current_bill_aye_votes = BillVote.objects.filter(
            vote="aye", bill=current_bill,
        ).order_by("-id")
    except ObjectDoesNotExist:
        current_bill_aye_votes = None

    try:
        current_bill_neutral_votes = BillVote.objects.filter(
            vote="neutral", bill=current_bill,
        ).order_by("-id")
    except ObjectDoesNotExist:
        current_bill_neutral_votes = None

    try:
        current_bill_nay_votes = BillVote.objects.filter(
            vote="nay", bill=current_bill,
        ).order_by("-id")
    except ObjectDoesNotExist:
        current_bill_nay_votes = None

    # Get the current user vote
    try:
        current_user_vote = BillVote.objects.get(
            voter=current_basic_user_profile, bill=current_bill,
        )
    except ObjectDoesNotExist:
        current_user_vote = None

    # Vote form processing
    if request.POST.get("basic_voting_bill_vote_submit_button"):
        hidden_vote_value = request.POST.get("hidden_vote_value")

        # check if the hidden vote value is empty
        if bool(hidden_vote_value) == False or hidden_vote_value == "":
            # do nothing since it is an empty cast vote
            pass
        else:
            # chekc if the bill is "passed" or "shelved" if it is you cannot
            # add more votes to it because the voting session has ended
            if current_bill.status == "passed" or current_bill.status == "shelved":
                pass
            else:
                # if there is no vote already create one. If there is a vote just
                # update the vote value. A user can only have one vote on each bill
                if bool(current_user_vote) == False or current_user_vote == None:
                    # create a new one
                    new_vote = BillVote(
                        voter=current_basic_user_profile,
                        bill=current_bill,
                        vote=hidden_vote_value,
                    )
                    new_vote.save()
                    # update the bill karma
                    if hidden_vote_value == "aye":
                        current_bill.karma += 1
                    elif hidden_vote_value == "neutral":
                        current_bill.karma += 0
                    elif hidden_vote_value == "nay":
                        current_bill.karma -= 1
                    current_bill.save()
                    # new notification about the bill
                    new_notification = NotificationBase(
                        notification_owner=current_basic_user_profile,
                        notified_user=current_bill.sponsor,
                        status="congress_bill_vote",
                        congress_bill_vote=new_vote,
                    )
                    new_notification.save()
                    return HttpResponseRedirect(
                        "/voting/congress/bill/read/" + str(current_bill.id) + "/"
                    )
                else:
                    # check if the current newly cast vote is the same as your
                    # previous vote if it is do not update it since you cannot
                    # spam and bruteforce the karma
                    if hidden_vote_value == current_user_vote.vote:
                        pass
                    else:
                        # update the bill karma
                        if hidden_vote_value == "aye":
                            current_bill.karma += 1
                        elif hidden_vote_value == "neutral":
                            if current_user_vote.vote == "aye":
                                current_bill.karma -= 1
                            elif current_user_vote.vote == "nay":
                                current_bill.karma += 1
                        elif hidden_vote_value == "nay":
                            current_bill.karma -= 1
                        current_bill.save()

                    # update the vote
                    current_user_vote.vote = hidden_vote_value
                    current_user_vote.save()
                    return HttpResponseRedirect(
                        "/voting/congress/bill/read/" + str(current_bill.id) + "/"
                    )

    # Delete request form processing
    if request.POST.get("basic_voting_bill_delete_request_submit_btn"):
        # check if the user is the owner of the bill
        if current_bill.sponsor == current_basic_user_profile:
            # check if there is a vote on the bill
            try:
                current_votes = BillVote.objects.filter(
                    bill=current_bill
                )
            except ObjectDoesNotExist:
                current_votes = None

            # if there is no vote than delete the bill
            if bool(current_votes) == False or current_votes == []:
                current_bill.delete()
                return HttpResponseRedirect("/voting/congress/0/")
            else:
                # if there is a vote submit a delete request
                new_delete_request = BillDeleteRequest(
                    bill=current_bill
                )
                new_delete_request.save()
                return HttpResponseRedirect("/voting/congress/0/")
        else:
            pass

    data = {
        "current_basic_user": current_basic_user,
        "current_basic_user_profile": current_basic_user_profile,
        "current_teacher_profile": current_teacher_profile,
        "current_bill": current_bill,
        "current_bill_aye_votes": current_bill_aye_votes,
        "current_bill_neutral_votes": current_bill_neutral_votes,
        "current_bill_nay_votes": current_bill_nay_votes,
        "aye_amount": len(current_bill_aye_votes),
        "neutral_amount": len(current_bill_neutral_votes),
        "nay_amount": len(current_bill_nay_votes),
        "current_user_vote": current_user_vote,
        "current_bill_history": current_bill_history,
        "current_bill_history_empty": current_bill_history_empty,
    }

    if current_basic_user == None:
        return HttpResponseRedirect("/auth/login/")
    else:
        return render(request, "basic_voting_sys/read_bill.html", data)


def basic_update_bill(request, bill_id):
    """
    in this view the user an update their bill if it is theirs
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

    # Update form processing
    empty_input = False
    bill_is_not_owned = False

    if request.POST.get("basic_voting_bill_update_submit"):
        title = request.POST.get("title")
        content = request.POST.get("content")

        # check if the bill is the current users
        if current_bill.sponsor == current_basic_user_profile:
            # check if the the inputs are empty
            if bool(title) == False or title == "" \
               or bool(content) == False or content == "":
                empty_input = True
            else:
                # create a new history record
                new_history_record = BillUpdateHistory(
                    bill=current_bill,
                    title=current_bill.title,
                    content=current_bill.content
                )
                new_history_record.save()
                # update the bill and return the bill's page
                current_bill.title = title
                current_bill.content = content
                current_bill.save()
                return HttpResponseRedirect(
                    "/voting/congress/bill/read/" + str(current_bill.id) + "/"
                )
        else:
            bill_is_not_owned = True

    data = {
        "current_basic_user": current_basic_user,
        "current_basic_user_profile": current_basic_user_profile,
        "current_teacher_profile": current_teacher_profile,
        "current_bill": current_bill,
        "empty_input": empty_input,
        "bill_is_not_owned": bill_is_not_owned,
    }

    if current_basic_user == None:
        return HttpResponseRedirect("/auth/login/")
    else:
        return render(request, "basic_voting_sys/update_bill.html", data)


def basic_bill_landing_page(request, page):
    """
    in this view the users can see the top-most voted bills on the site.
    Descends from the most upvotes to least
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

    # Get all of the bills in a ordered array from the newly created one
    # At every page there will be 45 entries so always multiply it by that and
    # then reduce your objects
    current_page = page
    previous_page = page-1
    next_page = page+1

    # Get all the voting status bills
    bill_records_starting_point = current_page * 46
    bill_records_ending_point = bill_records_starting_point + 46

    try:
        current_page_bills = Bill.objects.filter(
            status="voting"
        ).order_by("-karma")[bill_records_starting_point:bill_records_ending_point]
    except ObjectDoesNotExist:
        current_page_bills = None

    # Bill votes
    bill_votes = {}
    for bill in current_page_bills:
        aye_votes = BillVote.objects.filter(bill=bill, vote="aye")
        nay_votes = BillVote.objects.filter(bill=bill, vote="nay")
        total_vote_value = len(aye_votes) - len(nay_votes)
        bill_votes[bill.id] = total_vote_value

    data = {
        "current_basic_user": current_basic_user,
        "current_basic_user_profile": current_basic_user_profile,
        "current_teacher_profile": current_teacher_profile,
        "current_page": current_page,
        "previous_page": previous_page,
        "next_page": next_page,
        "current_page_bills": current_page_bills,
        "bill_votes": bill_votes,
    }

    if current_basic_user == None:
        return HttpResponseRedirect("/auth/login/")
    else:
        return render(request, "basic_voting_sys/landing_page.html", data)


def basic_bill_new_page(request, page):
    """
    in this page the users can see all of the newly created bills
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

    # Get all of the bills in a ordered array from the newly created one
    # At every page there will be 45 entries so always multiply it by that and
    # then reduce your objects
    current_page = page
    previous_page = page-1
    next_page = page+1

    bill_records_starting_point = current_page * 46
    bill_records_ending_point = bill_records_starting_point + 46
    try:
        current_page_bills = Bill.objects.all().order_by("-id")[bill_records_starting_point:bill_records_ending_point]
    except ObjectDoesNotExist:
        current_page_bills = None

    # Bill votes
    bill_votes = {}
    for bill in current_page_bills:
        aye_votes = BillVote.objects.filter(bill=bill, vote="aye")
        nay_votes = BillVote.objects.filter(bill=bill, vote="nay")
        total_vote_value = len(aye_votes) - len(nay_votes)
        bill_votes[bill.id] = total_vote_value

    data = {
        "current_basic_user": current_basic_user,
        "current_basic_user_profile": current_basic_user_profile,
        "current_teacher_profile": current_teacher_profile,
        "current_page_bills": current_page_bills,
        "current_page": current_page,
        "previous_page": previous_page,
        "next_page": next_page,
        "bill_votes": bill_votes,
    }

    if current_basic_user == None:
        return HttpResponseRedirect("/auth/login/")
    else:
        return render(request, "basic_voting_sys/new_page.html", data)


def basic_bill_passed_page(request, page):
    """
    in this view the users can see the passed bills instead of all of the bills
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

    # Get the PASSED bills
    # At every page there will be 45 entries so always multiply it by that and
    # then reduce your objects
    current_page = page
    previous_page = page-1
    next_page = page+1

    bill_records_starting_point = current_page * 46
    bill_records_ending_point = bill_records_starting_point + 46

    try:
        current_page_bills = Bill.objects.filter(
            status="passed"
        ).order_by("-id")[bill_records_starting_point:bill_records_ending_point]
    except ObjectDoesNotExist:
        current_page_bills = None

    # Bill votes
    bill_votes = {}
    for bill in current_page_bills:
        aye_votes = BillVote.objects.filter(bill=bill, vote="aye")
        nay_votes = BillVote.objects.filter(bill=bill, vote="nay")
        total_vote_value = len(aye_votes) - len(nay_votes)
        bill_votes[bill.id] = total_vote_value

    data = {
        "current_basic_user": current_basic_user,
        "current_basic_user_profile": current_basic_user_profile,
        "current_teacher_profile": current_teacher_profile,
        "current_page_bills": current_page_bills,
        "current_page": current_page,
        "previous_page": previous_page,
        "next_page": next_page,
        "bill_votes": bill_votes,
    }

    if current_basic_user == None:
        return HttpResponseRedirect("/auth/login/")
    else:
        return render(request, "basic_voting_sys/passed_page.html", data)


def basic_bill_shelved_page(request, page):
    """
    in this view the users can see the shelved (arcived) bills
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

    # Get the SHELVED bills
    # At every page there will be 45 entries so always multiply it by that and
    # then reduce your objects
    current_page = page
    previous_page = page-1
    next_page = page+1

    bill_records_starting_point = current_page * 46
    bill_records_ending_point = bill_records_starting_point + 46

    try:
        current_page_bills = Bill.objects.filter(
            status="shelved"
        ).order_by("-id")[bill_records_starting_point:bill_records_ending_point]
    except ObjectDoesNotExist:
        current_page_bills = None

    # Bill votes
    bill_votes = {}
    for bill in current_page_bills:
        aye_votes = BillVote.objects.filter(bill=bill, vote="aye")
        nay_votes = BillVote.objects.filter(bill=bill, vote="nay")
        total_vote_value = len(aye_votes) - len(nay_votes)
        bill_votes[bill.id] = total_vote_value

    data = {
        "current_basic_user": current_basic_user,
        "current_basic_user_profile": current_basic_user_profile,
        "current_teacher_profile": current_teacher_profile,
        "current_page_bills": current_page_bills,
        "current_page": current_page,
        "previous_page": previous_page,
        "next_page": next_page,
        "bill_votes": bill_votes,
    }

    if current_basic_user == None:
        return HttpResponseRedirect("/auth/login/")
    else:
        return render(request, "basic_voting_sys/shelved_page.html", data)
