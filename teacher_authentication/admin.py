from django.contrib import admin
from .models import TeacherApplication, TeacherUserProfile

# Register your models here.
admin.site.register(TeacherApplication)
admin.site.register(TeacherUserProfile)
