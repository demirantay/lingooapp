# Main Imports

# Django Imports
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# My Module Imports
from profile_settings.models import BasicUserProfile


# Track Record
# ----------------
# Records all the days you have done lessons and how much have you done
class LessonTrackRecord(models.Model):
    id = models.AutoField(primary_key=True)
    creation_date = models.DateField(default=timezone.now)
    user = models.ForeignKey(BasicUserProfile, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)

    def __str__(self):
        return "user: " + str(self.user) + " | amount: " + str(self.amount)
