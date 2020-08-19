# Main Imports

# Django Imports
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# My Module Imports
from profile_settings.models import BasicUserProfile
from basic_language_explore.models import Language


# Forum Post
# -------------
# This model holds the records of basic users forum posts
class ForumPost(models.Model):
    id = models.AutoField(primary_key=True)
    creation_date = models.DateField(default=timezone.now)
    user_profile = models.ForeignKey(BasicUserProfile, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    post_title = models.CharField(max_length=500, blank=True, null=True)
    content = models.TextField(max_length=10000, blank=True, null=True)
    karma = models.IntegerField(default=0)
    is_pinned = models.BooleanField(default=False)

    def __str__(self):
        return "id: " + str(self.id) + " | " + str(self.post_title)


# Forum Comment
# -------------
# This model holds the records of basic users forum posts Comments
class ForumComment(models.Model):
    id = models.AutoField(primary_key=True)
    creation_date = models.DateField(default=timezone.now)
    user_profile = models.ForeignKey(BasicUserProfile, on_delete=models.CASCADE)
    post = models.ForeignKey(ForumPost, on_delete=models.CASCADE)
    content = models.TextField(max_length=1000, blank=True, null=True)
    karma = models.IntegerField(default=0)

    def __str__(self):
        return "comment id: " + str(self.id) + " | post: " + str(self.post)
