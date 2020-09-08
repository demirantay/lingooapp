# Main Imports

# Django Imports
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# My Module Imports
from teacher_language_explore.models import TeacherLanguageCourse


'''
    Not including a basic user because I am going to use
    django's User model for it.
'''


# Teacher User Profile
# -----------------
# This model holds the users with the teacher profile yes, all of the users
# inheirt the same Django User model however every profile is used for
# different panels.
class TeacherUserProfile(models.Model):
    # O2One relationship with django's user model
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    creation_date = models.DateField(default=timezone.now)
    id = models.AutoField(primary_key=True)

    # Teacher Signup-Permissions (only assigned by the user)
    is_permitted_to_login = models.BooleanField(default=False)

    # Application & Signup Information
    native_language = models.CharField(max_length=200, blank=True, null=True)
    course_language = models.CharField(max_length=300, blank=True, null=True)
    course_speakers_language = models.CharField(max_length=300, blank=True, null=True)
    first_name = models.CharField(max_length=300, blank=True, null=True)
    last_name = models.CharField(max_length=300, blank=True, null=True)
    occupation = models.CharField(max_length=300, blank=True, null=True)
    email = models.CharField(max_length=100, blank=False, null=False)

    teacher_course = models.ForeignKey(TeacherLanguageCourse, on_delete=models.CASCADE, blank=True, null=True)

    # Edit Profile -- settings
    profile_photo = models.ImageField(
        upload_to="teacher_profile_photo/", blank=True, null=True
    )
    bio = models.TextField(blank=True, null=True)
    personal_url = models.CharField(max_length=1000, blank=True, null=True)
    location = models.CharField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return "Profile ID: " + str(self.id) + " | User: " + str(self.user)


# Teacher Application
# -----------------
# This model holds the records for applications for teacher positions.
class TeacherApplication(models.Model):
    id = models.AutoField(primary_key=True)
    creation_date = models.DateField(default=timezone.now)
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)

    # application info
    course_language = models.CharField(max_length=300, blank=False, null=False)
    course_speakers_language = models.CharField(max_length=300, blank=False, null=False)
    native_language = models.CharField(max_length=200, blank=False, null=False)
    course_language_why_are_you_interested_text = models.TextField(max_length=1000)
    speakers_language_why_are_you_interested_text = models.TextField(max_length=1000)
    email = models.CharField(max_length=300, blank=False, null=False)
    older_than_13 = models.BooleanField(default=False)

    def __str__(self):
        return "Application ID: " + str(self.id)
