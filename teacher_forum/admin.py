from django.contrib import admin
from .models import TeacherForumPost, TeacherForumComment

# Register your models here.
admin.site.register(TeacherForumPost)
admin.site.register(TeacherForumComment)
