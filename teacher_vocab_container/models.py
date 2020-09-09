# Main Imports

# Django Imports
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# My Module Imports
from teacher_authentication.models import TeacherUserProfile
from teacher_language_explore.models import TeacherLanguageCourse


# Teacher Vocabulary Container Words
# -----------------------
# this model holds the words of the vocabulary contianer, again this is the
# teacher one that keeeps on changing and developing, the student one is more
# static so it will be defined in another apps model
class TeacherVocabularyContainer(models.Model):
    id = models.AutoField(primary_key=True)
    creation_date = models.DateField(default=timezone.now)
    course = models.ForeignKey(TeacherLanguageCourse, on_delete=models.CASCADE, blank=True, null=True)
    teacher = models.ForeignKey(TeacherUserProfile, on_delete=models.CASCADE, blank=True, null=True)
    word = models.CharField(max_length=500, blank=True, null=True)
    LEVEL_CHOICES = (
        ("a0", "a0"),
        ("a1", "a1"),
        ("a2", "a2"),
        ("b1", "b1"),
        ("b2", "b2"),
        ("c1", "c1"),
        ("advanced", "advanced"),
    )
    level = models.CharField(max_length=100, default="a0", choices=LEVEL_CHOICES)

    def __str__(self):
        return "Word: " + self.word + " | course: " + str(self.course)
