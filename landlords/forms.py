from django import forms
from .models import *
from property.models import *

class PropertyOwnerForm(forms.ModelForm):
    class Meta:
        model = PropertyOwner
        fields = '__all__'

class AgentForm(forms.ModelForm):
    class Meta:
        model = Agent
        fields = '__all__'

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = '__all__'
