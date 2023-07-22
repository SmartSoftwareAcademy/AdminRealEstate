from django.contrib import admin
from .models import StaffSalaryPayment


# Register your models here.
@admin.register(StaffSalaryPayment)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('staff', 'month', 'year','date_of_pyament','net_pay')
    list_filter = ('month', 'year','date_of_pyament')
    search_fields = ('staff__user__username', 'staff__user__email')  # Example search fields, adjust as needed

    def save_model(self, request, obj, form, change):
        obj.calculate_net_pay()  # Calculate the net salary
        super().save_model(request, obj, form, change)

