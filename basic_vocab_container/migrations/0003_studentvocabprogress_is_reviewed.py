# Generated by Django 3.1 on 2020-09-26 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic_vocab_container', '0002_basicvocaberrorreport'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentvocabprogress',
            name='is_reviewed',
            field=models.BooleanField(default=False),
        ),
    ]
