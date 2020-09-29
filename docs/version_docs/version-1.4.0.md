# `Version 1.4.0`

## Design Summary

In this update I added the first basic learning content for the main users of
the site. Because I needed to give at least one content for the main users.
It is a simple repetition-based vocabulary lessons with reviewing in between.
And also in order to deliver that in the background I added the course, enrollments, ... etc. and the other neccessary background mechanisms for the language courses.

## Frontend Updates

At this point there is no libraries or any other frontend framework implemented in the site. It uses vanilla html, css, javascript and uses Django template engine to display the data not JSON API format

Newly Additions to the template folder:

- For "language explore" Template and Static directories named `basic_language_explore`
  - language explore page
  - info page
- For "vocab container" Template and Static directories named `basic_vocab_container`
  - learning start page
  - lesson learning page
  - reviewing page
- For "home learning tree" Template and Static directories named `home`
  - Modified: placeholder home page
  - added a learning tree page

## Backend Updates

`basic_language_explore` feature new models:

```python
# Language
# ------------
# This models holds all of the language records such as English, spanish
# french, turkish .. etc. It will expand as the time goes on but for now it
# will just have the language's name, flag images, and some chid relationships
class Language(models.Model):
    id = models.AutoField(primary_key=True)
    creation_date = models.DateField(default=timezone.now)
    name = models.CharField(max_length=100, blank=False, null=False)
    flag = models.ImageField(
        upload_to="flag_photo/basic/",
        blank=True,
        null=True
    )

    def __str__(self):
        return "Language: " + str(self.name)


# Language Course
# ---------------
# This model holds all of the production-level courses for the langauges
class BasicLanguageCourse(models.Model):
    id = models.AutoField(primary_key=True)
    creation_date = models.DateField(default=timezone.now)
    course_language = models.CharField(max_length=300, blank=False, null=False)
    course_speakers_language = models.CharField(max_length=300, blank=False, null=False)
    about_language = models.TextField(default="...")

    def __str__(self):
        return "Course Language: " + self.course_language + \
               " | Speakers: " + self.course_speakers_language


# Student
# -------------
# This model holds all of the language learners recordsd and is a child
# relationship to Language reocrds and holds a one-2-one relationship with
# a single basic user profile. By the way this is completly different than the
# langauge model that is based in the `teacher_langauge_explore` it is mostly
# the development staged langauges this is the production records that the user
# 's user
class Student(models.Model):
    id = models.AutoField(primary_key=True)
    creation_date = models.DateField(default=timezone.now)
    langauge = models.ForeignKey(Language, on_delete=models.CASCADE)
    basic_user_profile = models.ForeignKey(
        BasicUserProfile,
        on_delete=models.CASCADE,
    )
    course = models.ForeignKey(
        BasicLanguageCourse,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    def __str__(self):
        return "id: " + str(self.id) + " | Basic User Profile: " + \
                str(self.basic_user_profile)

```

`basic_language_explore` feature new views:
- Language Explore page: (`basic_language_explore`) -- url path: `language/explore/<str:speaker_language>/`
- language Info page: (`basic_language_explore_info`) -- url path: `language/explore/info/<str:course_language>/<str:speakers_language>/`

`basic_vocab_container` feature new models:

```python
# Basic Vocabulary Container
# ---------
# Basic Vocabualry Continer that has all of the words to be learned
class BasicVocabularyContainer(models.Model):
    id = models.AutoField(primary_key=True)
    creation_date = models.DateField(default=timezone.now)
    course = models.ForeignKey(BasicLanguageCourse, on_delete=models.CASCADE, blank=True, null=True)
    word = models.CharField(max_length=500, blank=True, null=True)
    word_translation = models.CharField(max_length=500, blank=True, null=True)
    LEVEL_CHOICES = (
        ("a0", "a0"),
        ("a1", "a1"),
        ("a2", "a2"),
        ("b1", "b1"),
        ("b2", "b2"),
        ("c1", "c1"),
        ("advanced", "advanced"),
    )
    level = models.CharField(max_length=100, default="a0", choices=LEVEL_CHOICES)

    def __str__(self):
        return "word: " + self.word + " || " + self.level + " || course: " \
                + str(self.course)


# Student Voacb Progress
# -----------
# This model will hold the records of the students progresses in each
# vocabulary course.
class StudentVocabProgress(models.Model):
    id = models.AutoField(primary_key=True)
    creation_date = models.DateField(default=timezone.now)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, blank=True, null=True)
    vocab_container_word = models.ForeignKey(BasicVocabularyContainer, on_delete=models.CASCADE, blank=True, null=True)
    is_learned = models.BooleanField(default=False)
    is_reviewed = models.BooleanField(default=False)

    def __str__(self):
        return "student: " + str(self.student)
        + " | word: " + str(self.vocab_container_word.word)


# Basic Vocab Error Reports
class BasicVocabErrorReport(models.Model):
    id = models.AutoField(primary_key=True)
    creation_date = models.DateField(default=timezone.now)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, blank=True, null=True)
    course = models.ForeignKey(BasicLanguageCourse, on_delete=models.CASCADE, blank=True, null=True)
    vocab_container = models.ForeignKey(BasicVocabularyContainer, on_delete=models.CASCADE, blank=True, null=True)
    error_report = models.TextField(default="...")

    def __str__(self):
        return "Error id: " + str(self.id) + " | " + self.error_report
```

`basic_vocab_container` feature new views:
- Learning Lesson Start page: (`basic_vocab_learn_start`) -- url: `vocab/learn/start/<str:cefr_level>/<str:course_language>/<str:speakers_langauge>/`
- Learning Lesson page: (`basic_vocab_learn`) -- url: `vocab/learn/<str:cefr_level>/<str:course_language>/<str:speakers_langauge>/`
- Review Lesson page: (`basic_vocab_review`) -- url: `vocab/review/<str:course_language>/<str:speakers_langauge>/`

`home` feature new models:

```python
# no changes have been applied to this apps models.py
```

`home` feature new views:
- Home Placeholder page: (`index`) -- url: `/`
- Learning Tree page (`learn_index`) -- url: `home/<str:course_language>/<str:speakers_language>/`


## DevOps Updates

At this version I haven't implemented anything regarding DevOps.

## Mobile Updates

At this version I haven't implemented anything regarding mobile.

## Security

I just scanned it with OWASP zap, I havent implemented anything at the moment.
