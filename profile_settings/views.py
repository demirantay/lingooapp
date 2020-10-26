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
from utils.session_utils import get_current_user, get_current_user_profile
from utils.session_utils import get_current_teacher_user_profile
from utils.access_control import delete_teacher_user_session
from utils.auth_utils import get_banned_words


def profile_settings_edit_profile(request):
    """
    In this view the user can change its main settings such as email, username,
    full name, bio but not password or SMS_n_notifications
    """
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

    # Edit Profile form processing
    empty_credentials = False
    invalid_credentials = False
    username_taken = False
    email_taken = False

    if request.POST.get("profile_edit_submit_btn"):
        profile_photo = request.FILES.get("profile_photo")
        full_name = request.POST.get("full_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        bio = request.POST.get("bio")
        location = request.POST.get("location")
        personal_link = request.POST.get("personal_link")

        # check if username and email are empty if it is empty dont process
        if bool(username) == False or bool(email) == False:
            empty_credentials = True
        else:
            # chceck if the username contains banned words
            banned_words = get_banned_words()
            for word in banned_words:
                if username == word:
                    invalid_credentials = True

            if invalid_credentials == False:
                # check if the username already exists with User model
                try:
                    existing_user = User.objects.get(
                        username=username
                    )
                except ObjectDoesNotExist:
                    existing_user = None

                # check if the existing username is current_user if it is make
                # it none so that the form can upload the rest. Because if you
                # do not change it to none the form outputs red warning becuase
                # it found a username (which is your current username)
                if existing_user == current_basic_user:
                    existing_user = None

                if existing_user is None:
                    # username does not exits, good! Now check for email
                    # check if email already exists
                    try:
                        existing_email = User.objects.get(
                            email=email
                        )
                    except ObjectDoesNotExist:
                        existing_email = None

                    # check if the existing email is current_user's email if it
                    # is make it none so that the form can upload the rest.
                    # because if you do not change it to tnone the form outputs
                    # red warning because it found a email ( which is your own
                    # current email)
                    if existing_email == current_basic_user:
                        existing_email = None

                    if existing_email == None:
                        # try to get the current users settings if it exists
                        # upadte it if it doesnt exits create a new record
                        # for current user
                        if current_basic_user_profile == None:
                            # it doesnt exists so create one
                            new_settings = BasicUserProfile(
                                user=current_basic_user,
                                profile_photo=profile_photo,
                                username=username,
                                email=email,
                                bio=bio,
                                full_name=full_name,
                                personal_url=personal_link,
                                location=location
                            )
                            new_settings.save()
                            # Also update the Basic users email and username
                            current_basic_user.email = email
                            current_basic_user.username = username
                            current_basic_user.save()
                            return HttpResponseRedirect("/profile/foo/foo/")
                        else:
                            # it exists so instead of creating one update
                            current_basic_user_profile.profile_photo = profile_photo
                            current_basic_user_profile.username = username
                            current_basic_user_profile.email = email
                            current_basic_user_profile.bio = bio
                            current_basic_user_profile.full_name = full_name
                            current_basic_user_profile.personal_url = personal_link
                            current_basic_user_profile.location = location
                            current_basic_user_profile.save()
                            # Also update the Basic users email and username
                            current_basic_user.email = email
                            current_basic_user.username = username
                            current_basic_user.save()
                            return HttpResponseRedirect("/profile/foo/foo/")
                    else:
                        email_taken = True
                else:
                    username_taken = True
            else:
                invalid_credentials = True

    data = {
        "current_basic_user": current_basic_user,
        "current_basic_user_profile": current_basic_user_profile,
        "current_teacher_profile": current_teacher_profile,
        "empty_credentials": empty_credentials,
        "invalid_credentials": invalid_credentials,
        "username_taken": username_taken,
        "email_taken": email_taken,
    }

    if current_basic_user == None:
        return HttpResponseRedirect("/auth/login/")
    else:
        return render(request, "profile_settings/edit_profile.html", data)


def profile_settings_change_password(request):
    """
    In this page the user can change their password
    """
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

    # Change Password form processing
    empty_input = False
    old_password_not_matching = False
    new_password_not_matching = False
    less_than_8_chars = False
    contains_digit = True
    username_password_similar = False

    if request.POST.get("change_password_submit_btn"):
        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        new_password_again = request.POST.get("new_password_again")

        # check if the any of the inputs are empty
        if bool(old_password) == False \
           or bool(new_password) == False \
           or bool(new_password_again) == False:
            empty_input = True
        else:
            # check if the password is same as username
            if new_password == current_basic_user.username:
                username_password_similar = True
            else:
                # it is not similar now check if the old passowrd is matching
                # with the current user
                is_matching = current_basic_user.check_password(old_password)

                if is_matching == True:
                    # check if the new passwords match
                    if new_password == new_password_again:
                        # check if passwords is greater than 8 chars
                        if len(new_password) >= 8:
                            # check if the passwords contain any digit
                            # I will probably forget why i turned this into
                            # false but let me explain: if i do not turn
                            # this into false, and set it to false on top
                            # of the file the template uses the false value
                            # even there is no data in the form and outputs
                            # the red warnign sign saying the pwd needs
                            # digits. This way when the view loads it is
                            # set to true at the top therefore it does not
                            # get the red warning and I set it to false
                            # over here so that if the below loop does not
                            # find any digits in it the contains_digit will
                            # be set to false for the red warning template
                            contains_digit = False
                            for char in new_password:
                                if char.isdigit():
                                    contains_digit = True

                            if contains_digit == True:
                                # change the password and log the user out
                                current_basic_user.set_password(new_password)
                                current_basic_user.save()
                                return HttpResponseRedirect("/auth/logout/")
                            else:
                                contains_digit = False
                        else:
                            less_than_8_chars = True
                    else:
                        new_password_not_matching = True
                else:
                    old_password_not_matching = True

    data = {
        "current_basic_user": current_basic_user,
        "current_basic_user_profile": current_basic_user_profile,
        "current_teacher_profile": current_teacher_profile,
        "empty_input": empty_input,
        "old_password_not_matching": old_password_not_matching,
        "new_password_not_matching": new_password_not_matching,
        "less_than_8_chars": less_than_8_chars,
        "contains_digit": contains_digit,
        "username_password_similar": username_password_similar,
    }

    if current_basic_user == None:
        return HttpResponseRedirect("/auth/login/")
    else:
        return render(request, "profile_settings/change_password.html", data)


def profile_settings_email_sms(request):
    """
    In this page the member users can view and update their
    email and SMS settings
    """
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

    # Email and SMS form processing
    if request.POST.get("email_sms_submit_btn"):
        feedback_emails = request.POST.get("feedback_emails")
        reminder_emails = request.POST.get("reminder_emails")
        product_emails = request.POST.get("product_emails")
        news_emails = request.POST.get("news_emails")

        if feedback_emails == "true":
            current_basic_user_profile.feedback_emails = True
        else:
            current_basic_user_profile.feedback_emails = False

        if reminder_emails == "true":
            current_basic_user_profile.reminder_emails = True
        else:
            current_basic_user_profile.reminder_emails = False

        if product_emails == "true":
            current_basic_user_profile.product_emails = True
        else:
            current_basic_user_profile.product_emails = False

        if news_emails == "true":
            current_basic_user_profile.news_emails = True
        else:
            current_basic_user_profile.news_emails = False

        current_basic_user_profile.save()
        return HttpResponseRedirect("/profile/")

    data = {
        "current_basic_user": current_basic_user,
        "current_basic_user_profile": current_basic_user_profile,
        "current_teacher_profile": current_teacher_profile,
    }

    if current_basic_user == None:
        return HttpResponseRedirect("/auth/login/")
    else:
        return render(request, "profile_settings/email_sms.html", data)
