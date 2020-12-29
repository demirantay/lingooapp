# Main Imports

# Django Imports
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# My Module Imports
from profile_settings.models import BasicUserProfile
from forum.models import ForumComment, ForumCommentReply
from basic_voting_sys.models import BillVote
from basic_feedback.models import FeedbackComment, FeedbackDevAnswer
from basic_feedback.models import FeedbackCommentReply


# Notification Model
# -------------------
# Notification cells notify the user if there is a comment made on their post
# if they were mentioned .. etc.
class NotificationBase(models.Model):
    # Base fields for the notifications
    id = models.AutoField(primary_key=True)
    creation_date = models.DateField(default=timezone.now)
    is_read = models.BooleanField(default=False)
    notification_owner = models.ForeignKey(
        BasicUserProfile,
        on_delete=models.CASCADE,
        related_name="notification_owner"
    )
    notified_user = models.ForeignKey(
        BasicUserProfile,
        on_delete=models.CASCADE,
        related_name="notified_user"
    )
    STATUS_CHOICES = (
        ("undefined", "undefined"),
        ("forum_post_comment", "forum_post_comment"),
        ("forum_comment_reply", "forum_comment_reply"),
        ("congress_bill_vote", "congress_bill_vote"),
        ("feedback_comment", "feedback_comment"),
        ("feedback_comment_reply", "feedback_comment_reply"),
    )
    status = models.CharField(
        max_length=300,
        default="undefined",
        choices=STATUS_CHOICES
    )
    # Relative fields based on the status of the notification
    forum_post_comment = models.ForeignKey(
        ForumComment,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    forum_comment_reply = models.ForeignKey(
        ForumCommentReply,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    congress_bill_vote = models.ForeignKey(
        BillVote,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    feedback_comment = models.ForeignKey(
        FeedbackComment,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    feedback_comment_reply = models.ForeignKey(
        FeedbackCommentReply,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    def __str__(self):
        return "Notfied user: " + str(self.notified_user)


# Announcement Notification Model
# -------------------
# These announcaments appear on the homepage of every user
class AnnouncementNotification(models.Model):
    id = models.AutoField(primary_key=True)
    creation_date = models.DateField(default=timezone.now)
    title = models.CharField(max_length=100, blank=True, null=True)
    content = models.TextField(blank=True, null=True)

    def __str__(self):
        return "Announcement: " + str(self.title)


# Announcement IS READ Model
# -------------------
# This model holds the records of the suers who have read the announcements and
# dismissed them
class AnnouncementIsRead(models.Model):
    id = models.AutoField(primary_key=True)
    creation_date = models.DateField(default=timezone.now)
    announcement = models.ForeignKey(
        AnnouncementNotification,
        on_delete=models.CASCADE,
        blank=False,
        null=False
    )
    user_profile = models.ForeignKey(
        BasicUserProfile,
        on_delete=models.CASCADE,
        blank=False,
        null=False
    )

    def __str__(self):
        return "Dismisser: " + str(self.user_profile)
