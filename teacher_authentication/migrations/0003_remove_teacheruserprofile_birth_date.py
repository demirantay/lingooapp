# Generated by Django 3.1 on 2020-09-07 15:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teacher_authentication', '0002_auto_20200907_0755'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teacheruserprofile',
            name='birth_date',
        ),
    ]
