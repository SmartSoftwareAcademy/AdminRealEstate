from django import forms
from .models import *

class PropertyOwnerForm(forms.ModelForm):
    class Meta:
        model = PropertyOwner
        fields = ['name', 'contact_number']

class AgentForm(forms.ModelForm):
    class Meta:
        model = Agent
        fields = ['owner', 'name', 'contact_number']

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['owner', 'address', 'property_type', 'num_rooms', 'rental_price']
