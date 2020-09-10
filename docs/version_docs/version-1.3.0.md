# `Version 1.3.0`

## Design Summary

In this update I added a lot of additions to the site. Because I need a teacher panel so that the teachers can start building the language courses. I added an teacher: authentication gate, dashboard, profile, profile settings, profile status, forum, vocabulary pack builder.

## Frontend Updates

At this point there is no libraries or any other frontend framework implemented in the site. It uses vanilla html, css, javascript and uses Django template engine to display the data not JSON API format

Newly Additions to the template folder:

- For "teacher authentication" Template and Static directories named `teacher_authentication`
  - apply page
  - login page
  - signup page
  - welcome page
- For "teacher dashboard" Template and Static directories named `teacher_dashboard`
  - announcament page
- For "teacher profile settings" Template and Static directories named `teacher_profile_settings`
  - edit profile page
- For "teacher profile" Template and Static directories named `teacher_profile`
  - overview page
  - other user profile overview page
- For "teacher language explore" Template and Static directories named `teacher_language_explore`
  - course overview page
  - course status page
  - course status update page
- For "teacher public about" Template and Static directories named `teacher_public_about`
  - course status
  - landing page
- For "teacher vocabulary builder" Template and Static directories named `teacher_vocab_container`
  - overview page
  - edit word page
- For "teacher forum" Template and Static directories named `teacher_forum`
  - landing page
  - create page
  - read page
  - update page

## Backend Updates

`teacher_authentication` feature new models:

```python
'''
    Not including a basic user because I am going to use
    django's User model for it.
'''


# Teacher User Profile
# -----------------
# This model holds the users with the teacher profile yes, all of the users
# inheirt the same Django User model however every profile is used for
# different panels.
class TeacherUserProfile(models.Model):
    # O2One relationship with django's user model
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    creation_date = models.DateField(default=timezone.now)
    id = models.AutoField(primary_key=True)

    # Teacher Signup-Permissions (only assigned by the user)
    is_permitted_to_login = models.BooleanField(default=False)

    # Application & Signup Information
    native_language = models.CharField(max_length=200, blank=True, null=True)
    course_language = models.CharField(max_length=300, blank=True, null=True)
    course_speakers_language = models.CharField(max_length=300, blank=True, null=True)
    first_name = models.CharField(max_length=300, blank=True, null=True)
    last_name = models.CharField(max_length=300, blank=True, null=True)
    occupation = models.CharField(max_length=300, blank=True, null=True)
    email = models.CharField(max_length=100, blank=False, null=False)

    teacher_course = models.ForeignKey(TeacherLanguageCourse, on_delete=models.CASCADE, blank=True, null=True)

    # Edit Profile -- settings
    profile_photo = models.ImageField(
        upload_to="teacher_profile_photo/", blank=True, null=True
    )
    bio = models.TextField(blank=True, null=True)
    personal_url = models.CharField(max_length=1000, blank=True, null=True)
    location = models.CharField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return "Profile ID: " + str(self.id) + " | User: " + str(self.user)


# Teacher Application
# -----------------
# This model holds the records for applications for teacher positions.
class TeacherApplication(models.Model):
    id = models.AutoField(primary_key=True)
    creation_date = models.DateField(default=timezone.now)
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)

    # application info
    course_language = models.CharField(max_length=300, blank=False, null=False)
    course_speakers_language = models.CharField(max_length=300, blank=False, null=False)
    native_language = models.CharField(max_length=200, blank=False, null=False)
    course_language_why_are_you_interested_text = models.TextField(max_length=1000)
    speakers_language_why_are_you_interested_text = models.TextField(max_length=1000)
    email = models.CharField(max_length=300, blank=False, null=False)
    older_than_13 = models.BooleanField(default=False)

    def __str__(self):
        return "Application ID: " + str(self.id)
```

`teacher_authentication` feature new views:
- Apply page: (`teacher_apply`) -- url path: `contrib/apply/`
- Login page: (`teacher_login`) -- url path: `teacher/login/`
- Logout page: (`teacher_logout`) -- url path: `teacher/logout/`
- Thanks page: (`application_thank_you_page`) -- url path: `contrib/apply/thanks/`

`teacher_dashboard` feature new models:

```python
# Dashboard Announcament Model
# -----------------
# This model holds the records for the announcaments that are created
class DashboardAnnouncament(models.Model):
    creation_date = models.DateField(default=timezone.now)
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    teacher = models.ForeignKey(TeacherUserProfile, on_delete=models.CASCADE, blank=True, null=True)
    course_language = models.CharField(max_length=300, blank=True, null=True)
    course_speakers_language = models.CharField(max_length=300, blank=True, null=True)
    content = models.TextField(blank=True, null=True)

    def __str__(self):
        return "id: " + str(self.id) + " | course_language: " + \
                self.course_language + " | course_speakers_language: " + \
                self.course_speakers_language
```

`teacher_dashboard` feature new views:
- Dashboard page: (`teacher_dashboard_announcament`) -- url path: `teacher/dashboard/announcament/`

`teacher_profile_settings` feature new models:

```python
# There is no new model additions in this app
```

`teacher_profile_settings` feature new views:
- Edit Profile page: (`teacher_profile_settings_edit_profile`) -- url path: `teacher/profile/settings/edit_profile/`

`teacher_profile` feature new models:

```python
# There is no new model additions in this app
```

`teacher_profile` feature new views:
- Profile page: (`teacher_profile_overview`) -- url path: `teacher/profile/`
- Other User Profile page: (`teacher_profile_other_user_overview`) -- url path: `teacher/profile/<str:other_user_username>`

`teacher_language_explore` feature new models:

```python
# Teacher Language Course Model
# ------------------
# This view is not a public course model, I am councisly choosing not to
# connect the students language course one to the teachers one because I want
# the teachers one to be more of a development course rather than a static
# production like one which is how the student langauge course is designed
# because student's courses content should not change daily
class TeacherLanguageCourse(models.Model):
    id = models.AutoField(primary_key=True)
    creation_date = models.DateField(default=timezone.now)
    course_language = models.CharField(max_length=300, blank=False, null=False)
    course_speakers_language = models.CharField(max_length=300, blank=False, null=False)

    # Development Progress
    a0 = models.IntegerField(default=0)
    a1 = models.IntegerField(default=0)
    a2 = models.IntegerField(default=0)
    b1 = models.IntegerField(default=0)
    b2 = models.IntegerField(default=0)
    c1 = models.IntegerField(default=0)

    def __str__(self):
        return "Course Language: " + self.course_language + \
               " | Speakers: " + self.course_speakers_language


# Teacher Language Course Status Update
# ----------------
# This model holds the status updates for the specific courses
class CourseStatusUpdate(models.Model):
    id = models.AutoField(primary_key=True)
    creation_date = models.DateField(default=timezone.now)
    course = models.ForeignKey(TeacherLanguageCourse, on_delete=models.CASCADE, blank=True, null=True)
    # If you do not import the model like the following it creates
    # a circular import and does not migrate models
    teacher = models.ForeignKey("teacher_authentication.TeacherUserProfile", on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=200, null=False, blank=False, default="")
    content = models.TextField()
```

`teacher_language_explore` feature new views:
- Teacher course overview: (`teacher_course_overview`) -- url path: `teacher/course/overview/`
- Teacher course status: (`teacher_course_status`) -- url path: `teacher/course/status/<str:language>/<str:speakers_language>/`
- Teacher course status update: (`teacher_course_status_update`) -- url path: `teacher/course/status/update/`

`teacher_public_about` feature new models:

```python
# There is no new model additions in this app
```

`teacher_public_about` feature new views:
- Public landing page: (`teacher_public_landing_page`) -- url path: `contrib/`
- Public course status: (`teacher_public_course_status`) -- url path: `contrib/course/status/<str:language>/<str:speakers_language>/`

`teacher_vocab_container` feature new models:

```python
# Teacher Vocabulary Container Words
# -----------------------
# this model holds the words of the vocabulary contianer, again this is the
# teacher one that keeeps on changing and developing, the student one is more
# static so it will be defined in another apps model
class TeacherVocabularyContainer(models.Model):
    id = models.AutoField(primary_key=True)
    creation_date = models.DateField(default=timezone.now)
    course = models.ForeignKey(TeacherLanguageCourse, on_delete=models.CASCADE, blank=True, null=True)
    teacher = models.ForeignKey(TeacherUserProfile, on_delete=models.CASCADE, blank=True, null=True)
    word = models.CharField(max_length=500, blank=True, null=True)
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
        return "Word: " + self.word + " | course: " + str(self.course)
```

`teacher_vocab_container` feature new views:
- Vocab container overview page: (`teacher_vocab_container_overview`) -- url path: `teacher/vocab/container/overview/`
- Vocab container edit page: (`teacher_vocab_container_edit`) -- url path: `teacher/vocab/container/edit/<int:word_id>/<str:word>/`

`teacher_forum` feature new models:

```python
# Teacher Forum Post
# -------------
# This model holds the records of teacher users forum posts
class TeacherForumPost(models.Model):
    id = models.AutoField(primary_key=True)
    creation_date = models.DateField(default=timezone.now)
    teacher = models.ForeignKey(TeacherUserProfile, on_delete=models.CASCADE, blank=True, null=True)
    course = models.ForeignKey(TeacherLanguageCourse, on_delete=models.CASCADE, blank=True, null=True)
    post_title = models.CharField(max_length=500, blank=True, null=True)
    content = models.TextField(max_length=10000, blank=True, null=True)
    karma = models.IntegerField(default=0)

    def __str__(self):
        return "id: " + str(self.id) + " | title: " + self.post_title


# Teacher Forum Comment
# -------------
# This model holds the records of teacher users forum posts Comments
class TeacherForumComment(models.Model):
    id = models.AutoField(primary_key=True)
    creation_date = models.DateField(default=timezone.now)
    teacher = models.ForeignKey(TeacherUserProfile, on_delete=models.CASCADE, blank=True, null=True)
    post = models.ForeignKey(TeacherForumPost, on_delete=models.CASCADE, blank=True, null=True)
    content = models.TextField(max_length=1000, blank=True, null=True)
    karma = models.IntegerField(default=0)

    def __str__(self):
        return "comment id: " + str(self.id) + " | post: " + str(self.post)
```

`teacher_forum` feature new views:
- Landing page: (`teacher_forum_landing_page`) -- url path: `teacher/forum/<int:page>/`
- Create page: (`teacher_forum_create`) -- url path: `teacher/forum/create/`
- Read page: (`teacher_forum_read`) -- url path: `teacher/forum/read/<int:post_id>/`
- Update page: (`teacher_forum_update`) -- url path: `teacher/forum/update/<int:post_id>/`

## DevOps Updates

At this version I haven't implemented anything regarding DevOps.

## Mobile Updates

At this version I haven't implemented anything regarding mobile.

## Security

I just scanned it with OWASP zap, I havent implemented anything at the moment.
