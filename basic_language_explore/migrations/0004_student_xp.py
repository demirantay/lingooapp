# Generated by Django 3.1 on 2020-10-23 03:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic_language_explore', '0003_auto_20200917_0628'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='xp',
            field=models.IntegerField(default=0),
        ),
    ]