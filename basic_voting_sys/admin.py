from django.contrib import admin
from .models import Bill, LastBillCreationDate, BillVote, BillUpdateHistory

# Register your models here.
admin.site.register(Bill)
admin.site.register(LastBillCreationDate)
admin.site.register(BillVote)
admin.site.register(BillUpdateHistory)
