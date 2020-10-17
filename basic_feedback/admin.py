from django.contrib import admin
from .models import Feedback, FeedbackDevAnswer, FeedbackComment
from .models import FeedbackCommentReply

# Register your models here.
admin.site.register(Feedback)
admin.site.register(FeedbackDevAnswer)
admin.site.register(FeedbackComment)
admin.site.register(FeedbackCommentReply)
