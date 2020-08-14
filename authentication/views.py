# Main Imports

# Django Imports
from django.shortcuts import render, get_object_or_404, HttpResponse
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.core.files import File
from django.contrib.auth.models import User

# My Module Imports
from utils.auth_utils import get_banned_words
from profile_settings.models import BasicUserProfile


def signup(request):
    """
    users can use this page to signup to the platform and create accounts
    """
    # admin user session pop
    # admin user session pop
    # Deleting any sessions regarding top-tier type of users

    # Deleting sessions regarding basic users
    if "basic_user_email" in request.session:
        del request.session["basic_user_email"]
        del request.session["basic_user_username"]
        del request.session["basic_user_logged_in"]

    # Signup Form Processing
    invalid_credentials = False
    credentials_taken = False

    banned_words = get_banned_words()

    if request.POST.get("signup_form_submit_btn"):
        username= request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password_again = request.POST.get("re_entered_password")

        # First check if any of the input are empty
        if bool(username) == False \
           or bool(email) == False \
           or bool(password) == False \
           or bool(password_again) == False:
            invalid_credentials = True
        else:
            # check if the username or passowrd are the same
            if username == password:
                invalid_credentials = True
            else:
                # then check if the paswords match
                if password != password_again:
                    invalid_credentials = True
                else:
                    # then check if the username contains any banned words
                    contains_banned_words = False
                    for word in banned_words:
                        if word == username:
                            contains_banned_words = True
                    if contains_banned_words == True:
                        invalid_credentials = True
                    else:
                        # check if the same username or email exists if it
                        # does do not log it to the database it already exists
                        try:
                            existing_username = User.objects.get(
                                username=username
                            )
                        except ObjectDoesNotExist:
                            existing_username = None

                        try:
                            existing_email = User.objects.get(email=email)
                        except ObjectDoesNotExist:
                            existing_email = None

                        if existing_username != None or existing_email != None:
                            credentials_taken = True
                        else:
                            # check if passwords is greater than 8 chars
                            if len(password) < 8:
                                invalid_credentials = True
                            else:
                                # check if the password contains any digits
                                contains_digit = False
                                for char in password:
                                    if char.isdigit():
                                        contains_digit = True

                                if contains_digit == True:
                                    # create new User instance
                                    # user create_user() method of User object
                                    # because otherwise password is not getting
                                    # stored properly or gets hashed
                                    new_user = User.objects.create_user(
                                        username=username,
                                        email=email,
                                        password=password
                                    )
                                    # create new BasicUserProfile instance
                                    # also get the new user and add that to
                                    # the one-2-one relationship between user
                                    # and it's settings
                                    new_user = User.objects.get(
                                        email=email,
                                        username=username
                                    )
                                    new_settings = BasicUserProfile()
                                    new_settings.username = username
                                    new_settings.email = email
                                    new_settings.user = new_user
                                    new_settings.save()
                                    # create the sessions
                                    request.session["basic_user_email"] = new_user.email
                                    request.session["basic_user_username"] = new_user.username
                                    request.session["basic_user_logged_in"] = True
                                    # redirect to welcome page
                                    return HttpResponseRedirect("/auth/welcome/")
                                else:
                                    invalid_credentials = True

        # check if the password is in common passwords
        # ... havent implemented this yet

        # Preventing brute force
        # ... havent implemented this yet

        # check if the email is @...com
        # ... havent implemented this yet.

    data = {
        "invalid_credentials": invalid_credentials,
        "credentials_taken": credentials_taken,
    }

    return render(request, "authentication/signup.html", data)


def login(request):
    """
    Login page where the users can login to the site
    """
    # admin user session pop
    # admin user session pop
    # Deleting any sessions regarding top-tier type of users

    # Deleting sessions regarding basic users
    if "basic_user_email" in request.session:
        del request.session["basic_user_email"]
        del request.session["basic_user_username"]
        del request.session["basic_user_logged_in"]

    # Login Form Processing
    invalid_credentials = False

    if request.POST.get("login_form_submit_btn"):
        username = request.POST.get("username")
        password = request.POST.get("password")

        # checking if the inputs are empty
        if bool(username) == False or bool(password) == False:
            invalid_credentials = True
        else:
            # Check if the user credits are right and if they
            # are log the user into the system and add sessions
            try:
                user = User.objects.get(username=username)
            except ObjectDoesNotExist:
                user = None

            if user == None:
                invalid_credentials = True
            else:
                # check password if it matches
                # redirect to home with sessions
                is_valid = user.check_password(password)

                if is_valid == True:
                    # update sessions
                    # update sessions
                    request.session["basic_user_email"] = user.email
                    request.session["basic_user_username"] = user.username
                    request.session["basic_user_logged_in"] = True
                    return HttpResponseRedirect("/forum/")
                else:
                    invalid_credentials = True

    # Preventing brute force
    # ... havent implemented this yet

    data = {
        "invalid_credentials": invalid_credentials,
    }

    return render(request, "authentication/login.html", data)


def logout(request):
    """
    if users visit this page it logs her out.
    """
    # Deleting sessions regarding basic users
    if "basic_user_email" in request.session:
        del request.session["basic_user_email"]
        del request.session["basic_user_username"]
        del request.session["basic_user_logged_in"]

    return HttpResponseRedirect("/")


def welcome(request):
    """
    users contact this page after they signup. This page makes them choose
    their first language
    """

    data = {}
    return render(request, "authentication/welcome.html", data)
