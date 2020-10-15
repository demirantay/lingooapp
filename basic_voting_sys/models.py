# Main Imports

# Django Imports
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from profile_settings.models import BasicUserProfile

# My Module Imports


# Bill Model
# -------------------
# A bill is a record that is createdd by the users and they are usually a
# request from the developers weather it is a feature request, a feature that
# they do not like ... etc
class Bill(models.Model):
    id = models.AutoField(primary_key=True)
    creation_date = models.DateField(default=timezone.now)
    sponsor = models.ForeignKey(BasicUserProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=True, blank=True)
    content = models.TextField(default="...", null=True, blank=True)
    STATUS_CHOICES = (
        ("voting", "voting"),
        ("passed", "passed"),
        ("shelved", "shelved"),
    )
    status = models.CharField(max_length=100, default="voting",
                              choices=STATUS_CHOICES)
    CATEGORY_CHOICES = (
        ("new_feature", "New Feature"),
        ("small_addition", "Small Addition"),
        ("feature_complaint", "Feature Complaint"),
        ("small_removal", "Small Removal"),
        ("feature_removal", "Feature Removal"),
    )
    category = models.CharField(max_length=100, default="new_feature",
                                choices=CATEGORY_CHOICES)

    def __str__(self):
        return "Bill id: " + str(self.id)


# Bill Last Add Date
class LastBillCreationDate(models.Model):
    id = models.AutoField(primary_key=True)
    user_profile = models.OneToOneField(BasicUserProfile, on_delete=models.CASCADE)
    creation_date = models.DateField(default=timezone.now, null=True, blank=True)

    def __str__(self):
        return "user: " + str(self.user_profile) + " | last creation: " + \
                str(self.creation_date)
