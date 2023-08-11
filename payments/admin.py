from django.contrib import admin
from .models import *


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('invoice','transaction_code', 'description', 'amount','outstanding_balance','payment_method','date_paid')
    list_filter = ('transaction_code', 'transaction_code', 'amount','outstanding_balance','date_paid')
    search_fields = ('invoice__invoice_id', 'transaction_code')

# @admin.register(RentDeposits)
# class RentDepositsAdmin(admin.ModelAdmin):
#     list_display = ('tenant','amount', 'date_paid')
#     list_filter = ('tenant', 'amount', 'date_paid')
#     search_fields = ('tenant__user__username', 'lease__property__address')