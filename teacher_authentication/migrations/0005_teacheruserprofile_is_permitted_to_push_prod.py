# Generated by Django 3.1 on 2020-11-03 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher_authentication', '0004_teacheruserprofile_teacher_course'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacheruserprofile',
            name='is_permitted_to_push_prod',
            field=models.BooleanField(default=False),
        ),
    ]