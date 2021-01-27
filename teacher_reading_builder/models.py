# Main Imports

# Django Imports
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# My Module Imports
from teacher_authentication.models import TeacherUserProfile
from teacher_language_explore.models import TeacherLanguageCourse


# Teacher Reading Lesson
# ---------------
# This model holds all of the lessons of the reading part of the application
class TeacherReadingLesson(models.Model):
    id = models.AutoField(primary_key=True)
    creation_date = models.DateField(default=timezone.now)
    course = models.ForeignKey(
        TeacherLanguageCourse,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    teacher = models.ForeignKey(
        TeacherUserProfile,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    title = models.CharField(max_length=200)

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
        return "Course: " + str(self.course) + " | title: " + self.title


# Teacher Reading Lesson Sentence
# ------------------
# This lesson holds the lessons for each of the lesson created above
class TeacherReadingLessonSentence(models.Model):
    id = models.AutoField(primary_key=True)
    creation_date = models.DateField(default=timezone.now)
    lesson = models.ForeignKey(
        TeacherReadingLesson,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    LEVEL_CHOICES = (
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
    )
    level = models.CharField(max_length=100, default="1", choices=LEVEL_CHOICES)
    question_prompt = models.CharField(max_length=2000)
    answer = models.CharField(max_length=2000)

    def __str__(self):
        return "Lesson: " + str(self.lesson) + " level: " + self.level + \
               "question_prompt: " + self.question_prompt


# Teacher Reading Lesson Sentence Tolerance
# ----------------------
# This lesson holds the tolerated typing for the answers of the snetences above
class TeacherReadingLessonSentenceTolerance(models.Model):
    id = models.AutoField(primary_key=True)
    creation_date = models.DateField(default=timezone.now)
    lesson_sentence = models.ForeignKey(
        TeacherReadingLessonSentence,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    tolerated_answer = models.CharField(max_length=2000)

    def __str__(self):
        return "Sentence: " + str(self.lesson_sentence)
