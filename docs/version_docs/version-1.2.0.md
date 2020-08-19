# `Version 1.2.0`

## Design Summary

In this update I added major additions to the site because i wanted to add a basic CRUD application that the users will be able to send me feedback and brainstorm ideas. Added a lot of features such as: authentication, profile settings, profile, forum

## Frontend Updates

At this point there is no libraries or any other frontend framework implemented in the site. It uses vanilla html, css, javascript and uses Django template engine to display the data not JSON API format

Newly Additions to the template folder:

- Template and Static directories named `authentication`
  - login page
  - signup page
  - welcome page
- Template and Static directories named `profile_settings`
  - edit profile page
  - email and sms page
  - change password page
- Templates and Static directories named `profile_app`
  - profile overview page
  - other user profile overview
- Templates and Static directories named `forum`
  - forum create page
  - forum read page
  - forum update page
  - forum landing page
  - forum category page

## Backend Updates

`Authentication` module new models:
```python
# There is no new models for this module Initially I created a model to use it
# for storing my Basic Users but instead I deleted it because of security
# vulnerability. I now just use djangos.auth.model - `User` model
```

`Authentication` module new views:
- Signup page: (`signup`) -- url path -- (`auth/signup/`)
- Login page: (`login`) -- url path -- (`auth/login/`)
- Logout page: (`logout`) -- url path -- (`auth/logout/`)
- Welcome page: (`welcome`) -- url path -- (`auth/welcome/`)

`Profile Settings` module new models:
```python
# Basic User Profile
# -------------
# This model holds the basis user profile such as email, username .. etc
# more complicated settigns such as privacy, sms ... etc. Basic profile is
# used and created for basic users.
class BasicUserProfile(models.Model):
    # O2One relationship with django's user model
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    creation_date = models.DateField(default=timezone.now)
    id = models.AutoField(primary_key=True)

    # Edit Profile -- settings
    profile_photo = models.ImageField(
        upload_to="profile_photo/", blank=True, null=True
    )
    username = models.CharField(max_length=100, blank=False, null=False)
    email = models.CharField(max_length=100, blank=False, null=False)
    bio = models.TextField(blank=True, null=True)
    full_name = models.CharField(max_length=100, blank=True, null=True)
    personal_url = models.CharField(max_length=1000, blank=True, null=True)
    location = models.CharField(max_length=1000, blank=True, null=True)

    # Email & SMS -- settings
    feedback_emails = models.BooleanField(default=False)
    reminder_emails = models.BooleanField(default=False)
    product_emails = models.BooleanField(default=False)
    news_emails = models.BooleanField(default=False)

    # Karma
    karma = models.IntegerField(default=0)

    def __str__(self):
        return "Settings id: " + str(self.id) + " | User: " + str(self.user)
```

`Profile Settings` module new views:
- Edit Profile page: (`profile_settings_edit_profile`) -- url path -- (`profile/settings/edit_profile/`)
- Change Password page: (`profile_settings_change_password`) -- url path -- (`profile/settings/change_password/`)
- Email and SMS page: (`profile_settings_email_sms`) -- url path -- (`profile/settings/email_sms/`)

`Profile` module new models:
```python
# I did not add any models because all the model that is needed is
# defined in profile settings app
```

`Profile` module new views:
- Profile Overview page: (`profile_overview`) -- url path -- (`profile/`)
- Other User Profile Overview page: (`other_user_profile_overview`) -- url path -- (`profile/<str:other_user_username>/`)

`Forum` new models:
```python
# Forum Post
# -------------
# This model holds the records of basic users forum posts
class ForumPost(models.Model):
    id = models.AutoField(primary_key=True)
    creation_date = models.DateField(default=timezone.now)
    user_profile = models.ForeignKey(BasicUserProfile, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    post_title = models.CharField(max_length=500, blank=True, null=True)
    content = models.TextField(max_length=10000, blank=True, null=True)
    karma = models.IntegerField(default=0)
    is_pinned = models.BooleanField(default=False)

    def __str__(self):
        return "id: " + str(self.id) + " | " + str(self.post_title)


# Forum Comment
# -------------
# This model holds the records of basic users forum posts Comments
class ForumComment(models.Model):
    id = models.AutoField(primary_key=True)
    creation_date = models.DateField(default=timezone.now)
    user_profile = models.ForeignKey(BasicUserProfile, on_delete=models.CASCADE)
    post = models.ForeignKey(ForumPost, on_delete=models.CASCADE)
    content = models.TextField(max_length=1000, blank=True, null=True)
    karma = models.IntegerField(default=0)

    def __str__(self):
        return "comment id: " + str(self.id) + " | post: " + str(self.post)
```

`Forum` new views:
- Forum Landing Page page: (`forum_landing_page`) -- url path -- (`forum/<int:page>/`)
- Forum Category Page page: (`forum_category_page`) -- url path -- (`forum/category/<str:category_language>/<int:page>/`)
- Forum Create page: (`forum_create`) -- url path -- (`forum/create/`)
- Forum Read page: (`forum_read`) -- url path -- (`forum/read/<int:post_id>/`)
- Forum Update page: (`forum_update`) -- url path -- (`forum/update/<int:post_id>/`)

## DevOps Updates

At this version I haven't implemented anything regarding DevOps.

## Mobile Updates

At this version I haven't implemented anything regarding mobile.

## Security

I just scanned it with OWASP zap, I havent implemented anything at the moment.
