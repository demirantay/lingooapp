# Generated by Django 3.1 on 2020-08-18 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0002_auto_20200818_0903'),
    ]

    operations = [
        migrations.AddField(
            model_name='forumpost',
            name='karma',
            field=models.IntegerField(default=0),
        ),
    ]
