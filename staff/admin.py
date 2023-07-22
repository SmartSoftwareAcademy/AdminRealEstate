from django.contrib import admin
from .models import *

class StaffSalaryInline(admin.TabularInline):
    model = StaffSalary
    extra = 0

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'position', 'date_of_joining')
    search_fields = ('user__username', 'position')
    inlines = (StaffSalaryInline,)

@admin.register(Earning)
class EarningAdmin(admin.ModelAdmin):
    list_display = ('name','amount')
    search_fields = ('name','amount')
    list_filter = ('name','amount')

@admin.register(Deduction)
class EarningAdmin(admin.ModelAdmin):
    list_display = ('name','amount')
    search_fields = ('name','amount')
    list_filter = ('name','amount')

@admin.register(StaffSalary)
class StaffSalaryAdmin(admin.ModelAdmin):
    list_display = ('staff','net_salary')
    search_fields = ('staff__user','net_salary')
    list_filter = ('staff','net_salary')
    readonly_fields = ('net_salary',)  # Optional: Make net_salary field read-only

    def save_model(self, request, obj, form, change):
        obj.calculate_net_pay()  # Calculate the net salary
        super().save_model(request, obj, form, change)

    def has_add_permission(self, request):
        return False  # Prevent adding new staff salary entries via the admin interface

    def has_delete_permission(self, request, obj=None):
        return True  # Prevent deleting staff salary entries via the admin interface

# admin.site.register(StaffSalary, StaffSalaryAdmin)
