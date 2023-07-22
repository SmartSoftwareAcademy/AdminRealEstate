from django import forms
from .models import Lease, LeaseTerm
from django.forms import inlineformset_factory,modelformset_factory

class LeaseForm(forms.ModelForm):
    class Meta:
        model = Lease
        fields = '__all__'

LeaseTermFormset=inlineformset_factory(Lease,LeaseTerm,fields=("term_number","late_payment_fine","utilities_amount","uilities_description","term_description","accepted"),extra=1)

