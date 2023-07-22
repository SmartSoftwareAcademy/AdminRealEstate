from django.contrib import admin
from .models import *


@admin.register(RentPayment)
class RentPaymentAdmin(admin.ModelAdmin):
    list_display = ('tenant', 'lease', 'amount', 'date_paid')
    list_filter = ('tenant', 'lease', 'amount', 'date_paid')
    search_fields = ('tenant__user__username', 'lease__property__address')

@admin.register(RentDeposits)
class RentDepositsAdmin(admin.ModelAdmin):
    list_display = ('tenant','amount', 'date_paid')
    list_filter = ('tenant', 'amount', 'date_paid')
    search_fields = ('tenant__user__username', 'lease__property__address')