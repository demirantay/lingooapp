# Main Imports

# Django Imports
from django.db import models
from django.utils import timezone
from profile_settings.models import BasicUserProfile

# My Module Imports


# Feedback Model
# ----------------
# This is the model that the users can create feedbacks for the devs of theSite
class Feedback(models.Model):
    id = models.AutoField(primary_key=True)
    creation_date = models.DateField(default=timezone.now)
    user = models.ForeignKey(BasicUserProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=True, blank=True, default="...")
    content = models.TextField(default="...", null=True, blank=True)
    views = models.IntegerField(default=0)

    def __str__(self):
        return "Id: " + str(self.id) + " | user: " + str(self.user.username) \
               + " | title: " + self.title


# Feedback Dev Answer
# -----------------
# This model holds the records for the dev answers of the feedback models
class FeedbackDevAnswer(models.Model):
    id = models.AutoField(primary_key=True)
    creation_date = models.DateField(default=timezone.now)
    feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE)
    content = models.TextField(default="...", null=True, blank=True)

    def __str__(self):
        return "Feedback ID: " + str(self.feedback.id)


# Feedback Comment
# -----------------
# This model holds the records for the feedback posts comments
class FeedbackComment(models.Model):
    id = models.AutoField(primary_key=True)
    creation_date = models.DateField(default=timezone.now)
    comment_owner = models.ForeignKey(BasicUserProfile, on_delete=models.CASCADE)
    feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE)
    content = models.TextField(default="...", null=True, blank=True)
    karma = models.IntegerField(default=0)

    def __str__(self):
        return "Feedback ID: " + str(self.feedback.id) + " | Comment ID: " \
               + str(self.id)


# Feedback Comment Reply
# ------------------
# This model holds the records for the replies for the feedback comments
class FeedbackCommentReply(models.Model):
    id = models.AutoField(primary_key=True)
    creation_date = models.DateField(default=timezone.now)
    comment = models.ForeignKey(FeedbackComment, on_delete=models.CASCADE)
    feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE,
                                 null=True, blank=True)
    reply_owner = models.ForeignKey(BasicUserProfile, on_delete=models.CASCADE)
    content = models.TextField(default="...", null=True, blank=True)

    def __str__(self):
        return "Feedback ID: " + str(self.feedback.id) + " | Comment ID: " \
               + str(self.comment.id) + " | Reply ID: " + str(self.id)
