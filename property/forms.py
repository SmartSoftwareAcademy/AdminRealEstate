from django import forms
from django.forms import inlineformset_factory, modelformset_factory
from .models import *

class PropertyUnitForm(forms.ModelForm):
    class Meta:
        model = Units
        fields = '__all__'

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = fields = (
            'address',
            'property_type',
            'property_name',
            'description',
            'amenities',
            'property_status',
            'year_built',
            'square_footage',
            'is_featured',
        )

PropertyImagesFormSet = inlineformset_factory(Property, PropertyImages, fields=('image',), extra=1,can_delete=True)