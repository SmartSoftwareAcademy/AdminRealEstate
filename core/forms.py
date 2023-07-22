from .models import Testimonial
from django import forms
from tinymce.widgets import TinyMCE

class TestimonialForm(forms.ModelForm):
    content = forms.CharField(widget=TinyMCE(attrs={'cols':3, 'rows': 3}))
    class Meta:
        model = Testimonial
        fields = ['designation','rating', 'content']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rating'].widget.attrs.update({'class': 'form-control'})
        self.fields['designation'].widget.attrs.update({'class': 'form-control'})
