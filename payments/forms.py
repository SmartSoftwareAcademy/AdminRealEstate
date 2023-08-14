from django import forms
from .models import *

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ('invoice','amount','description','payment_method')

class MpesaNumberForm  (forms.Form):
    mpesa_number=forms.IntegerField(required=True,widget=forms.NumberInput(attrs={'class':'form-control'}))
    invoice_id=forms.IntegerField(required=True,widget=forms.NumberInput(attrs={'class':'form-control','type': 'hidden'}))
    amount=forms.IntegerField(required=True,widget=forms.NumberInput(attrs={'class':'form-control', 'type': 'hidden'}))
    description=forms.CharField(required=True,widget=forms.Textarea(attrs={'rows':3,'cols':20,'class':'form-control', 'type': 'hidden'}))
    send_mail=forms.BooleanField(required=False,widget=forms.CheckboxInput(attrs={'class':'form-input','checked': 'checked'}))

    class Meta:
        fields = ('mpesa_number','invoice_id','amount','description','send_mail')
