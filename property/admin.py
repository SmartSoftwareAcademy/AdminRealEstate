from django.contrib import admin
from .models import *


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('property_name','address', 'property_type', 'owner')
    list_filter = ('property_name','property_type', 'owner')
    search_fields = ('property_name','address', 'property_type', 'owner__name')

@admin.register(Units)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('title', 'unit_code', 'rental_price')
    list_filter = ('title', 'unit_code')
    search_fields = ('title', 'rental_price', 'unit_code')

@admin.register(PropertyImages)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('property', 'image')
    list_filter =  ('property', 'image')
    search_fields =  ('property', 'image')

@admin.register(PropertyUnitImages)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('property_unit', 'image')
    list_filter =  ('property_unit', 'image')
    search_fields =  ('property_unit', 'image')