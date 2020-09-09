# Main Imports

# Django Imports
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# My Module Imports
#from teacher_authentication.models import TeacherUserProfile


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

    # Development Progress
    a0 = models.IntegerField(default=0)
    a1 = models.IntegerField(default=0)
    a2 = models.IntegerField(default=0)
    b1 = models.IntegerField(default=0)
    b2 = models.IntegerField(default=0)
    c1 = models.IntegerField(default=0)

    def __str__(self):
        return "Course Language: " + self.course_language + \
               " | Speakers: " + self.course_speakers_language


# Teacher Language Course Status Update
# ----------------
# This model holds the status updates for the specific courses
class CourseStatusUpdate(models.Model):
    id = models.AutoField(primary_key=True)
    creation_date = models.DateField(default=timezone.now)
    course = models.ForeignKey(TeacherLanguageCourse, on_delete=models.CASCADE, blank=True, null=True)
    # If you do not import the model like the following it creates
    # a circular import and does not migrate models
    teacher = models.ForeignKey("teacher_authentication.TeacherUserProfile", on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=200, null=False, blank=False, default="")
    content = models.TextField()
