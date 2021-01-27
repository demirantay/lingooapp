from django.contrib import admin
from .models import TeacherReadingLesson, TeacherReadingLessonSentence
from .models import TeacherReadingLessonSentenceTolerance

# Register your models here.
admin.site.register(TeacherReadingLesson)
admin.site.register(TeacherReadingLessonSentence)
admin.site.register(TeacherReadingLessonSentenceTolerance)
