# Generated by Django 3.1 on 2020-10-17 11:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('basic_feedback', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedbackcommentreply',
            name='feedback',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='basic_feedback.feedback'),
        ),
    ]
