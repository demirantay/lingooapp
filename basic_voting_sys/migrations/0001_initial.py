# Generated by Django 3.1 on 2020-10-14 11:44

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('profile_settings', '0002_basicuserprofile_location'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('creation_date', models.DateField(default=django.utils.timezone.now)),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('content', models.TextField(blank=True, default='...', null=True)),
                ('status', models.CharField(choices=[('voting', 'voting'), ('passed', 'passed'), ('shelved', 'shelved')], default='voting', max_length=100)),
                ('sponsor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profile_settings.basicuserprofile')),
            ],
        ),
    ]
