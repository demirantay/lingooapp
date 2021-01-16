# Main Imports

# Django Imports
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# My Module Imports
from teacher_authentication.models import TeacherUserProfile


# Teacher - Dictionary
# ----------------
# In this model the teacher users can create new dictionaries but to be honest
# all of the dictionaries are created by the admin to avoid any spamming
class TeacherDictionary(models.Model):
    creation_date = models.DateField(default=timezone.now)
    id = models.AutoField(primary_key=True)
    dictionary_language = models.CharField(
        max_length=300,
        blank=True,
        null=True
    )
    dictionary_speakers_language = models.CharField(
        max_length=300,
        blank=True,
        null=True
    )

    def __str__(self):
        return "Dict: " + self.dictionary_language +  \
               "| Lang: " + self.dictionary_speakers_language


# Teacher - Dictionary Word
# --------------
# In this model the teachers can create new words for the dictionaries above
class TeacherDictionaryWord(models.Model):
    creation_date = models.DateField(default=timezone.now)
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    teacher = models.ForeignKey(TeacherUserProfile, on_delete=models.CASCADE)
    dictionary = models.ForeignKey(TeacherDictionary, on_delete=models.CASCADE)
    word = models.CharField(max_length=50, blank=True, null=True)
    translation = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return "Dict: " + str(self.dictionary) + "| word: " + self.word
