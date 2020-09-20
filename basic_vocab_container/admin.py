from django.contrib import admin
from .models import BasicVocabularyContainer, StudentVocabProgress

# Register your models here.
admin.site.register(BasicVocabularyContainer)
admin.site.register(StudentVocabProgress)
