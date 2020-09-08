# Main Imports

# Django Imports
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# My Module Imports


# Teacher Language Course Model
# ------------------
# This view is not a public course model, I am councisly choosing not to
# connect the students language course one to the teachers one because I want
# the teachers one to be more of a development course rather than a static
# production like one which is how the student langauge course is designed
# because student's courses content should not change daily
class TeacherLanguageCourse(models.Model):
    id = models.AutoField(primary_key=True)
    creation_date = models.DateField(default=timezone.now)
    course_language = models.CharField(max_length=300, blank=False, null=False)
    course_speakers_language = models.CharField(max_length=300, blank=False, null=False)

    def __str__(self):
        return "Course Language: " + self.course_language + \
               " | Speakers: " + self.course_speakers_language
