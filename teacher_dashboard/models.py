# Main Imports

# Django Imports
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# My Module Imports
from teacher_authentication.models import TeacherUserProfile


# Dashboard Announcament Model
# -----------------
# This model holds the records for the announcaments that are created
class DashboardAnnouncament(models.Model):
    creation_date = models.DateField(default=timezone.now)
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    teacher = models.ForeignKey(TeacherUserProfile, on_delete=models.CASCADE, blank=True, null=True)
    course_language = models.CharField(max_length=300, blank=True, null=True)
    course_speakers_language = models.CharField(max_length=300, blank=True, null=True)
    content = models.TextField(blank=True, null=True)

    def __str__(self):
        return "id: " + str(self.id) + " | course_language: " + \
                self.course_language + " | course_speakers_language: " + \
                self.course_speakers_language
