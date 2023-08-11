from django import forms
from django.forms.widgets import DateInput, TextInput
from django.forms import widgets
from django.forms.models import inlineformset_factory
from .models import Staff, StaffSalary

class StaffForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(StaffForm, self).__init__(*args, **kwargs)
        self.fields["date_of_joining"].widget = widgets.DateInput(attrs={"type": "date","class":"form-control"})

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


