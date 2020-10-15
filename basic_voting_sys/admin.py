from django.contrib import admin
from .models import Bill, LastBillCreationDate, BillVote, BillUpdateHistory
from .models import BillDeleteRequest

# Register your models here.
admin.site.register(Bill)
admin.site.register(LastBillCreationDate)
admin.site.register(BillVote)
admin.site.register(BillUpdateHistory)
admin.site.register(BillDeleteRequest)
