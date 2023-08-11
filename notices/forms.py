from django import forms
from .models import *
from django.forms.widgets import DateInput, TextInput
from django.forms import widgets
from tinymce.widgets import TinyMCE


class NoticeRequestForm(forms.ModelForm):
    description = forms.CharField(widget=TinyMCE(attrs={'cols': 3, 'rows': 3}))
    def __init__(self, *args, **kwargs):
        super(NoticeRequestForm, self).__init__(*args, **kwargs)
        self.fields["notice_date"].widget = widgets.DateInput(attrs={"type": "date","class":"form-control"})
    class Meta:
        model = Notice
        fields = "__all__"

class EnquirytForm(forms.ModelForm):
    message = forms.CharField(widget=TinyMCE(attrs={'cols': 3, 'rows': 3}))
    def __init__(self, *args, **kwargs):
        super(EnquirytForm, self).__init__(*args, **kwargs)
        #self.fields["notice_date"].widget = widgets.DateInput(attrs={"type": "date","class":"form-control"})
    class Meta:
        model = Enquiries
        fields = ['fullname','email', 'mobile_number', 'message']