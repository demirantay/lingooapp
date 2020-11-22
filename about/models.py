# Main Imports

# Django Imports
from django.db import models
from django.utils import timezone


# About - Contact Us Message
# ---------------
# This table holds records of user messages made in contact page
class ContactUsMessage(models.Model):
    id = models.AutoField(primary_key=True)
    creation_date = models.DateField(default=timezone.now)
    name = models.CharField(max_length=200, blank=True, null=True)
    email = models.CharField(max_length=300, blank=True, null=True)
    message = models.TextField(default="...", blank=True, null=True)

    def __str__(self):
        return str(self.name) + " | " + str(self.email)
