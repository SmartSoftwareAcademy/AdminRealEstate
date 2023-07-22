from django.contrib import admin
from .models import *

@admin.register(Lease)
class LeaseAdmin(admin.ModelAdmin):
    list_display = ('tenant', 'property_unit', 'start_date', 'end_date')
    list_filter = ('start_date', 'end_date')
    search_fields = ('tenant__user__username', 'property_unit__address')


@admin.register(LeaseTerm)
class LeaseTermAdmin(admin.ModelAdmin):
    list_display = ('term_number','lease', 'late_payment_fine')
    list_filter = ('term_number','lease', 'late_payment_fine')
    search_fields = ('term_number','lease', 'late_payment_fine')