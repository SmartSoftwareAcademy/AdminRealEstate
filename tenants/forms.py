from django import forms
from django.forms.widgets import DateInput, TextInput
from django.forms import widgets
from .models import *
from django.contrib.auth import get_user_model
from django.forms import inlineformset_factory, modelformset_factory

User=get_user_model()

class FormSettings(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormSettings, self).__init__(*args, **kwargs)
        # Here make some changes such as:
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'


class CustomUserForm(FormSettings):
    email = forms.EmailField(required=True)
    gender = forms.ChoiceField(choices=[('M', 'Male'), ('F', 'Female')])
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    other_name=forms.CharField(required=False)
    address = forms.CharField(widget=forms.Textarea)
    password = forms.CharField(widget=forms.PasswordInput)
    widget = {
        'password': forms.PasswordInput(),
    }
    profile_pic = forms.ImageField(required=False)
    def __init__(self, *args, **kwargs):
        super(CustomUserForm, self).__init__(*args, **kwargs)

        if kwargs.get('instance'):
            instance = kwargs.get('instance').user.__dict__
            self.fields['password'].required = False
            for field in CustomUserForm.Meta.fields:
                self.fields[field].initial = instance.get(field)
            if self.instance.pk is not None:
                self.fields['password'].widget.attrs['placeholder'] = "Fill this only if you wish to update password"

    def clean_email(self, *args, **kwargs):
        formEmail = self.cleaned_data['email'].lower()
        if self.instance.pk is None:  # Insert
            if User.objects.filter(email=formEmail).exists():
                raise forms.ValidationError(
                    "The given email is already registered")
        else:  # Update
            dbEmail = self.Meta.model.objects.get(
                id=self.instance.pk).user.email.lower()
            if dbEmail != formEmail:  # There has been changes
                if User.objects.filter(email=formEmail).exists():
                    raise forms.ValidationError(
                        "The given email is already registered")

        return formEmail

    class Meta:
        model = User
        fields = ['first_name', 'last_name','other_name', 'email',
                  'gender',  'password', 'profile_pic', 'address']

class TenantForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(TenantForm, self).__init__(*args, **kwargs)
        self.fields["date_of_birth"].widget = widgets.DateInput(attrs={"type": "date","class":"form-control"})
        self.fields["date_of_registration"].widget = widgets.DateInput(attrs={"type": "date","class":"form-control"})

    class Meta(CustomUserForm.Meta):
        model = Tenant
        fields =  CustomUserForm.Meta.fields +['date_of_birth','date_of_registration', 'mobile_number','National_ID','others']
TenantKinFormSet = inlineformset_factory(Tenant, Tenant_Kin, fields=('name', 'phone', 'relation', 'emergency_name', 'emergency_phone_number', 'emergency_email', 'emergency_adress', 'emergency_physical_adress',), extra=1,can_delete=True)

class TenantKinForm(forms.ModelForm):
    class Meta:
        model = Tenant_Kin
        fields = ['name', 'phone', 'relation', 'emergency_name', 'emergency_phone_number', 'emergency_email', 'emergency_adress', 'emergency_physical_adress']

class TenantEmploymentForm(forms.ModelForm):
    class Meta:
        model = Tenant_Employment_Details
        fields = ['employment_status', 'emplyment_title', 'employment_postion', 'employer_contact', 'employer_email', 'employer_address']

class TenantBusinessForm(forms.ModelForm):
    class Meta:
        model = Tenant_Business_Details
        fields = ['business_name', 'license_number', 'tax_id', 'business_email', 'business_address', 'business_description']