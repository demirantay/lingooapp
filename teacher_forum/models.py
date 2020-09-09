# Main Imports

# Django Imports
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# My Module Imports
from teacher_language_explore.models import TeacherLanguageCourse
from teacher_authentication.models import TeacherUserProfile


# Teacher Forum Post
# -------------
# This model holds the records of teacher users forum posts
class TeacherForumPost(models.Model):
    id = models.AutoField(primary_key=True)
    creation_date = models.DateField(default=timezone.now)
    teacher = models.ForeignKey(TeacherUserProfile, on_delete=models.CASCADE, blank=True, null=True)
    course = models.ForeignKey(TeacherLanguageCourse, on_delete=models.CASCADE, blank=True, null=True)
    post_title = models.CharField(max_length=500, blank=True, null=True)
    content = models.TextField(max_length=10000, blank=True, null=True)
    karma = models.IntegerField(default=0)

    def __str__(self):
        return "id: " + str(self.id) + " | title: " + self.post_title


# Teacher Forum Comment
# -------------
# This model holds the records of teacher users forum posts Comments
class TeacherForumComment(models.Model):
    id = models.AutoField(primary_key=True)
    creation_date = models.DateField(default=timezone.now)
    teacher = models.ForeignKey(TeacherUserProfile, on_delete=models.CASCADE, blank=True, null=True)
    post = models.ForeignKey(TeacherForumPost, on_delete=models.CASCADE, blank=True, null=True)
    content = models.TextField(max_length=1000, blank=True, null=True)
    karma = models.IntegerField(default=0)

    def __str__(self):
        return "comment id: " + str(self.id) + " | post: " + str(self.post)
