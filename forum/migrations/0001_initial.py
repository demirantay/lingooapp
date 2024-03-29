# Generated by Django 3.1 on 2020-08-18 09:03

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('basic_language_explore', '0002_auto_20200817_1159'),
        ('profile_settings', '0002_basicuserprofile_location'),
    ]

    operations = [
        migrations.CreateModel(
            name='ForumPost',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('creation_date', models.DateField(default=django.utils.timezone.now)),
                ('post_title', models.CharField(blank=True, max_length=500, null=True)),
                ('content', models.CharField(blank=True, max_length=10000, null=True)),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basic_language_explore.language')),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profile_settings.basicuserprofile')),
            ],
        ),
    ]
