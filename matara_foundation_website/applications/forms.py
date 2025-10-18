from django import forms
from .models import Application

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['full_name', 'email', 'phone_number', 'county', 'date_of_birth', 'application_file']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }
