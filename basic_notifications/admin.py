from django.contrib import admin
from .models import NotificationBase, AnnouncementNotification
from .models import AnnouncementIsRead

# Register your models here.
admin.site.register(NotificationBase)
admin.site.register(AnnouncementNotification)
admin.site.register(AnnouncementIsRead)
