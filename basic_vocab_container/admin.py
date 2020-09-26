from django.contrib import admin
from .models import BasicVocabularyContainer, StudentVocabProgress
from .models import BasicVocabErrorReport

# Register your models here.
admin.site.register(BasicVocabularyContainer)
admin.site.register(StudentVocabProgress)
admin.site.register(BasicVocabErrorReport)
