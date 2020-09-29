from django.contrib import admin
from .models import BasicVocabularyContainer, StudentVocabProgress
from .models import BasicVocabErrorReport

# Register your models here.
# admin.site.register(BasicVocabularyContainer)
admin.site.register(StudentVocabProgress)
admin.site.register(BasicVocabErrorReport)


@admin.register(BasicVocabularyContainer)
class BasicVocabularyContainer(admin.ModelAdmin):
    list_display = ('level', 'word', 'course',)
    list_filter = ('level', 'course')
