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


# Language Course
# ---------------
# This model holds all of the production-level courses for the langauges
class BasicLanguageCourse(models.Model):
    id = models.AutoField(primary_key=True)
    creation_date = models.DateField(default=timezone.now)
    course_language = models.CharField(max_length=300, blank=False, null=False)
    course_speakers_language = models.CharField(max_length=300, blank=False, null=False)
    about_language = models.TextField(default="...")

    def __str__(self):
        return "Course Language: " + self.course_language + \
               " | Speakers: " + self.course_speakers_language


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
    basic_user_profile = models.ForeignKey(
        BasicUserProfile,
        on_delete=models.CASCADE,
    )
    course = models.ForeignKey(
        BasicLanguageCourse,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    xp = models.IntegerField(default=0)
    LEVEL_CHOICES = (
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
        ("4", "4"),
        ("5", "5"),
        ("6", "6"),
        ("7", "7"),
        ("8", "8"),
        ("9", "9"),
        ("10", "10"),
        ("11", "11"),
        ("12", "12"),
        ("13", "13"),
        ("14", "14"),
        ("15", "15"),
        ("16", "16"),
        ("17", "17"),
        ("18", "18"),
        ("19", "19"),
        ("20", "20"),
        ("21", "21"),
        ("22", "22"),
        ("23", "23"),
        ("24", "24"),
        ("25", "25"),
        ("26", "26"),
        ("27", "27"),
        ("28", "28"),
        ("29", "29"),
        ("30", "30"),
        ("10", "10"),
        ("11", "11"),
        ("12", "12"),
        ("13", "13"),
        ("14", "14"),
        ("15", "15"),
        ("16", "16"),
        ("17", "17"),
        ("18", "18"),
        ("19", "19"),
        ("20", "20"),
        ("21", "21"),
        ("22", "22"),
        ("23", "23"),
        ("24", "24"),
        ("25", "25"),
        ("26", "26"),
        ("27", "27"),
        ("28", "28"),
        ("29", "29"),
        ("30", "30"),
        ("31", "31"),
        ("32", "32"),
        ("33", "33"),
        ("34", "34"),
        ("35", "35"),
        ("36", "36"),
        ("37", "37"),
        ("38", "38"),
        ("39", "39"),
        ("40", "40"),
        ("41", "41"),
        ("42", "42"),
        ("43", "43"),
        ("44", "44"),
        ("45", "45"),
        ("46", "46"),
        ("47", "47"),
        ("48", "48"),
        ("49", "49"),
        ("50", "50"),
        ("61", "61"),
        ("62", "62"),
        ("63", "63"),
        ("64", "64"),
        ("65", "65"),
        ("66", "66"),
        ("67", "67"),
        ("68", "68"),
        ("69", "69"),
        ("70", "70"),
        ("71", "71"),
        ("72", "72"),
        ("73", "73"),
        ("74", "74"),
        ("75", "75"),
        ("76", "76"),
        ("77", "77"),
        ("78", "78"),
        ("79", "79"),
        ("80", "80"),
        ("81", "81"),
        ("82", "82"),
        ("83", "83"),
        ("84", "84"),
        ("85", "85"),
        ("86", "86"),
        ("87", "87"),
        ("88", "88"),
        ("89", "89"),
        ("90", "90"),
    )
    level = models.CharField(max_length=100, default="1",
                              choices=LEVEL_CHOICES)

    def __str__(self):
        return "id: " + str(self.id) + " | Basic User Profile: " + \
                str(self.basic_user_profile)
