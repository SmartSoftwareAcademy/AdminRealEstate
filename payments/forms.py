from django import forms
from .models import *

class RentPaymentForm(forms.ModelForm):
    class Meta:
        model = RentPayment
        fields = '__all__'

class RentDeposit(forms.ModelForm):
    class Meta:
        model = RentDeposits
        fields = '__all__'
