from django.contrib import admin
from .models import Bill, LastBillCreationDate

# Register your models here.
admin.site.register(Bill)
admin.site.register(LastBillCreationDate)
