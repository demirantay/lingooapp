# Generated by Django 3.1 on 2020-11-19 06:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('basic_voting_sys', '0007_bill_karma'),
        ('forum', '0006_auto_20201108_1240'),
        ('basic_feedback', '0002_feedbackcommentreply_feedback'),
        ('basic_notifications', '0003_auto_20201119_0637'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feedbackcommentnotification',
            name='feedback_comment',
        ),
        migrations.RemoveField(
            model_name='feedbackcommentnotification',
            name='notification_base',
        ),
        migrations.RemoveField(
            model_name='feedbackcommentreplynotification',
            name='comment_reply',
        ),
        migrations.RemoveField(
            model_name='feedbackcommentreplynotification',
            name='notification_base',
        ),
        migrations.RemoveField(
            model_name='feedbackdevanswernotification',
            name='feedback_dev_answer',
        ),
        migrations.RemoveField(
            model_name='feedbackdevanswernotification',
            name='notification_base',
        ),
        migrations.RemoveField(
            model_name='forumcommentreplynotification',
            name='comment_reply',
        ),
        migrations.RemoveField(
            model_name='forumcommentreplynotification',
            name='notification_base',
        ),
        migrations.RemoveField(
            model_name='forumpostcommentnotification',
            name='notification_base',
        ),
        migrations.RemoveField(
            model_name='forumpostcommentnotification',
            name='post_comment',
        ),
        migrations.AddField(
            model_name='notificationbase',
            name='congress_bill_vote',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='basic_voting_sys.billvote'),
        ),
        migrations.AddField(
            model_name='notificationbase',
            name='feedback_comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='basic_feedback.feedbackcomment'),
        ),
        migrations.AddField(
            model_name='notificationbase',
            name='feedback_comment_reply',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='basic_feedback.feedbackcommentreply'),
        ),
        migrations.AddField(
            model_name='notificationbase',
            name='feedback_dev_answer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='basic_feedback.feedbackdevanswer'),
        ),
        migrations.AddField(
            model_name='notificationbase',
            name='forum_comment_reply',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='forum.forumcommentreply'),
        ),
        migrations.AddField(
            model_name='notificationbase',
            name='forum_post_comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='forum.forumcomment'),
        ),
        migrations.DeleteModel(
            name='CongressBillVoteNotification',
        ),
        migrations.DeleteModel(
            name='FeedbackCommentNotification',
        ),
        migrations.DeleteModel(
            name='FeedbackCommentReplyNotification',
        ),
        migrations.DeleteModel(
            name='FeedbackDevAnswerNotification',
        ),
        migrations.DeleteModel(
            name='ForumCommentReplyNotification',
        ),
        migrations.DeleteModel(
            name='ForumPostCommentNotification',
        ),
    ]