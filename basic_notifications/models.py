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

    def __str__(self):
        return "Notfied user: " + str(self.notified_user)


# Forum Post Comment Notification
class ForumPostCommentNotification(models.Model):
    notification_base = models.ForeignKey(NotificationBase, on_delete=models.CASCADE)
    post_comment = models.ForeignKey(ForumComment, on_delete=models.CASCADE)

    def __str__(self):
        return "Comment: " + str(self.post_comment)


# Forum Comment Reply Notification
class ForumCommentReplyNotification(models.Model):
    notification_base = models.ForeignKey(NotificationBase, on_delete=models.CASCADE)
    comment_reply = models.ForeignKey(ForumCommentReply, on_delete=models.CASCADE)

    def __str__(self):
        return "Reply: " + str(self.comment_reply)


# Congress Bill Vote Notification
class CongressBillVoteNotification(models.Model):
    notification_base = models.ForeignKey(NotificationBase, on_delete=models.CASCADE)
    bill_vote = models.ForeignKey(BillVote, on_delete=models.CASCADE)

    def __str__(self):
        return "Bill: " + str(self.bill_vote)


# Feedback Comment Notification
class FeedbackCommentNotification(models.Model):
    notification_base = models.ForeignKey(NotificationBase, on_delete=models.CASCADE)
    feedback_comment = models.ForeignKey(FeedbackComment, on_delete=models.CASCADE)

    def __str__(self):
        return "Feedback Comment: " + str(self.feedback_comment)


# Feedback Dev Answer Notification
class FeedbackDevAnswerNotification(models.Model):
    notification_base = models.ForeignKey(NotificationBase, on_delete=models.CASCADE)
    feedback_dev_answer = models.ForeignKey(FeedbackDevAnswer, on_delete=models.CASCADE)

    def __str__(self):
        return "Feedback Deb Answer: " + str(self.feedback_dev_answer)


# Feedback Comment Reply Notification
class FeedbackCommentReplyNotification(models.Model):
    notification_base = models.ForeignKey(NotificationBase, on_delete=models.CASCADE)
    comment_reply = models.ForeignKey(FeedbackCommentReply, on_delete=models.CASCADE)

    def __str__(self):
        return "Feedback Comment Reply: " + str(self.comment_reply)
