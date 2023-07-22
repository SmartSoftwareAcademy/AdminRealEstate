from django.contrib import admin
from .models import *


@admin.register(PropertyOwner)
class PropertyOwnerAdmin(admin.ModelAdmin):
    list_display = ('user', 'mobile_number')
    list_filter = ('user',)
    search_fields = ('user', 'mobile_number')

@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ('user','mobile_number', 'owner')
    list_filter = ('user','owner',)
    search_fields = ('user', 'mobile_number', 'owner')