from django import forms
from .models import *

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ('invoice','amount','description','payment_method')

class MpesaNumberForm  (forms.Form):
    mpesa_number=forms.IntegerField(required=True,widget=forms.NumberInput(attrs={'class':'form-control'}))
    class Meta:
        fields = ('mpesa_number')
