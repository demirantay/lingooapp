# Generated by Django 3.1 on 2020-11-18 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic_notifications', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notificationbase',
            name='status',
            field=models.CharField(choices=[('undefined', 'undefined'), ('forum_post_comment', 'forum_post_comment'), ('forum_comment_reply', 'forum_comment_reply'), ('congress_bill_vote', 'congress_bill_vote'), ('feedback_comment', 'feedback_comment'), ('feedback_dev_answer', 'feedback_dev_answer'), ('feedback_comment_reply', 'feedback_comment_reply')], default='undefined', max_length=300),
        ),
    ]
