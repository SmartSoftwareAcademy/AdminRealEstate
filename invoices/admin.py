from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display=('lease','invoice_type','amount','description','status','due_date','updated_at')
    list_filter=('lease','invoice_type','amount','description','status','due_date','updated_at')
    search_fields=('lease','invoice_type','amount','description','status','due_date','updated_at')