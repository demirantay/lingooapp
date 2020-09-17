from django.contrib import admin
from .models import Language, Student, BasicLanguageCourse

# Register your models here.
admin.site.register(Language)
admin.site.register(Student)
admin.site.register(BasicLanguageCourse)
