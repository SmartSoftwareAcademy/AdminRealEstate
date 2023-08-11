from django.contrib import admin
from .models import *

@admin.register(Notice)
class MaintenanceRequestAdmin(admin.ModelAdmin):
    list_display = ('notice_type','user', 'notice_date')
    list_filter = ('notice_date',)
    search_fields = ('tenant__user__username', 'property__address')

@admin.register(NoticeFeedback)
class MaintenanceRequestAdmin(admin.ModelAdmin):
    list_display = ('notice','reply', 'notice_date')
    list_filter = ('notice','reply')
    search_fields = ('notice', 'reply')


@admin.register(Enquiries)
class MaintenanceRequestAdmin(admin.ModelAdmin):
    list_display = ('fullname','email', 'message')
    list_filter = ('fullname','email')
    search_fields = ('fullname', 'message')