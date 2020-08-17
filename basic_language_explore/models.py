# Main Imports

# Django Imports
from django.db import models
from django.utils import timezone

# My Module Imports
from profile_settings.models import BasicUserProfile


# Language
# ------------
# This models holds all of the language records such as English, spanish
# french, turkish .. etc. It will expand as the time goes on but for now it
# will just have the language's name, flag images, and some chid relationships
class Language(models.Model):
    id = models.AutoField(primary_key=True)
    creation_date = models.DateField(default=timezone.now)
    name = models.CharField(max_length=100, blank=False, null=False)
    flag = models.ImageField(
        upload_to="flag_photo/basic/",
        blank=True,
        null=True
    )

    def __str__(self):
        return "Language: " + str(self.name)


# Student
# -------------
# This model holds all of the language learners recordsd and is a child
# relationship to Language reocrds and holds a one-2-one relationship with
# a single basic user profile. By the way this is completly different than the
# langauge model that is based in the `teacher_langauge_explore` it is mostly
# the development staged langauges this is the production records that the user
# 's user
class Student(models.Model):
    id = models.AutoField(primary_key=True)
    creation_date = models.DateField(default=timezone.now)
    langauge = models.ForeignKey(Language, on_delete=models.CASCADE)
    basic_user_profile = models.OneToOneField(
        BasicUserProfile,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return "id: " + str(self.id) + " | Basic User Profile: " + \
                str(self.basic_user_profile)
