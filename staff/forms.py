from django import forms
from django.forms.models import inlineformset_factory
from .models import Staff, StaffSalary

class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = '__all__'


class StaffSalaryForm(forms.ModelForm):
    class Meta:
        model = StaffSalary
        fields = ['earnings', 'deductions']
        # widgets = {
        #     'earnings': forms.NumberInput(attrs={'class': 'form-control'}),
        #     'deductions': forms.NumberInput(attrs={'class': 'form-control'}),
        # }

StaffSalaryFormSet = inlineformset_factory(Staff, StaffSalary, form=StaffSalaryForm, extra=1)


