from django.contrib import admin
from .models import NotificationBase, ForumPostCommentNotification
from .models import ForumCommentReplyNotification, CongressBillVoteNotification
from .models import FeedbackCommentNotification, FeedbackDevAnswerNotification
from .models import FeedbackCommentReplyNotification

# Register your models here.
admin.site.register(NotificationBase)
admin.site.register(ForumPostCommentNotification)
admin.site.register(ForumCommentReplyNotification)
admin.site.register(CongressBillVoteNotification)
admin.site.register(FeedbackCommentNotification)
admin.site.register(FeedbackDevAnswerNotification)
admin.site.register(FeedbackCommentReplyNotification)
