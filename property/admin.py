from django.contrib import admin
from .models import *


class PropertyImagesInline(admin.TabularInline):
    model = PropertyImages
    extra = 3  # Number of inline forms to display

class PropertyUnitImagesInline(admin.TabularInline):
    model = PropertyUnitImages
    extra = 3  # Number of inline forms to display

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    inlines = [PropertyImagesInline]
    list_display = ('property_name','address', 'property_type', 'owner')
    list_filter = ('property_name','property_type', 'owner')
    search_fields = ('property_name','address', 'property_type', 'owner__name')

@admin.register(Units)
class UnitAdmin(admin.ModelAdmin):
    inlines = [PropertyUnitImagesInline]
    list_display = ('title', 'unit_code', 'rental_price')
    list_filter = ('title', 'unit_code')
    search_fields = ('title', 'rental_price', 'unit_code')
