# Main Imports

# Django Imports
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# My Module Imports
from basic_language_explore.models import BasicLanguageCourse, Student


# Basic Vocabulary Container
# ---------
# Basic Vocabualry Continer that has all of the words to be learned
class BasicVocabularyContainer(models.Model):
    id = models.AutoField(primary_key=True)
    creation_date = models.DateField(default=timezone.now)
    course = models.ForeignKey(BasicLanguageCourse, on_delete=models.CASCADE, blank=True, null=True)
    word = models.CharField(max_length=500, blank=True, null=True)
    word_translation = models.CharField(max_length=500, blank=True, null=True)
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
        return "word: " + self.word + " || " + self.level + " || course: " \
                + str(self.course)


# Student Voacb Progress
# -----------
# This model will hold the records of the students progresses in each
# vocabulary course.
class StudentVocabProgress(models.Model):
    id = models.AutoField(primary_key=True)
    creation_date = models.DateField(default=timezone.now)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, blank=True, null=True)
    vocab_container_word = models.ForeignKey(BasicVocabularyContainer, on_delete=models.CASCADE, blank=True, null=True)
    is_learned = models.BooleanField(default=False)

    def __str__(self):
        return "student: " + str(self.student)
        + " | word: " + str(self.vocab_container_word.word)
