from django import forms
from .models import StaffSalaryPayment

class StaffPaymentForm(forms.ModelForm):
    class Meta:
        model = StaffSalaryPayment
        fields = ('staff','month','year')