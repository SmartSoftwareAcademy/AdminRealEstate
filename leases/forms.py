from django import forms
from django.forms.widgets import DateInput, TextInput
from django.forms import widgets
from .models import Lease, LeaseTerm
from django.forms import inlineformset_factory,modelformset_factory

class LeaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(LeaseForm, self).__init__(*args, **kwargs)
        self.fields["start_date"].widget = widgets.DateInput(attrs={"type": "date","class":"form-control"})
        self.fields["end_date"].widget = widgets.DateInput(attrs={"type": "date","class":"form-control"})

    class Meta:
        model = Lease
        fields = ('property_unit','tenant','start_date','end_date','monthly_rent','security_deposit','is_active')

LeaseTermFormset=inlineformset_factory(Lease,LeaseTerm,fields=("term_number","late_payment_fine","utilities_amount","uilities_description","term_description","accepted"),extra=1)

