from django.contrib import admin
from .models import *


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ('user','mobile_number', 'date_of_birth')
    list_filter = ('user',)
    search_fields = ('user__username', 'mobile_number')

admin.site.register(Tenant_Kin)
admin.site.register(Tenant_Employment_Details)
admin.site.register(Tenant_Business_Details)
