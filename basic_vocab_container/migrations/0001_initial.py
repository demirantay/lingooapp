# Generated by Django 3.1 on 2020-09-20 10:25

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('basic_language_explore', '0003_auto_20200917_0628'),
    ]

    operations = [
        migrations.CreateModel(
            name='BasicVocabularyContainer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('creation_date', models.DateField(default=django.utils.timezone.now)),
                ('word', models.CharField(blank=True, max_length=500, null=True)),
                ('word_translation', models.CharField(blank=True, max_length=500, null=True)),
                ('level', models.CharField(choices=[('a0', 'a0'), ('a1', 'a1'), ('a2', 'a2'), ('b1', 'b1'), ('b2', 'b2'), ('c1', 'c1'), ('advanced', 'advanced')], default='a0', max_length=100)),
                ('course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='basic_language_explore.basiclanguagecourse')),
            ],
        ),
        migrations.CreateModel(
            name='StudentVocabProgress',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('creation_date', models.DateField(default=django.utils.timezone.now)),
                ('is_learned', models.BooleanField(default=False)),
                ('student', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='basic_language_explore.student')),
                ('vocab_container_word', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='basic_vocab_container.basicvocabularycontainer')),
            ],
        ),
    ]
