from django.contrib import admin
from .models import ForumPost, ForumComment

# Register your models here.
admin.site.register(ForumPost)
admin.site.register(ForumComment)
