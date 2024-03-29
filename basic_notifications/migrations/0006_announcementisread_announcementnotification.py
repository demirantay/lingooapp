# Generated by Django 3.1 on 2020-12-29 09:26

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('profile_settings', '0002_basicuserprofile_location'),
        ('basic_notifications', '0005_auto_20201120_0821'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnnouncementNotification',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('creation_date', models.DateField(default=django.utils.timezone.now)),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('content', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='AnnouncementIsRead',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('creation_date', models.DateField(default=django.utils.timezone.now)),
                ('announcement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basic_notifications.announcementnotification')),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profile_settings.basicuserprofile')),
            ],
        ),
    ]
