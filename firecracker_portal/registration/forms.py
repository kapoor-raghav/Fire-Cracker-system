# registration/forms.py
from django import forms
from .models import CustomUserProfile
from .models import StallApplication
from django.contrib.auth.forms import UserCreationForm

class StallApplicationForm(forms.ModelForm):
    class Meta:
        model = StallApplication
        fields = ['stall_name', 'location', 'description', 'document']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            widget = field.widget
            # File inputs use Bootstrap's form-control-file
            if isinstance(widget, forms.ClearableFileInput):
                widget.attrs.update({'class': 'form-control-file'})
            else:
                # Default to standard Bootstrap form-control
                existing = widget.attrs.get('class', '')
                classes = (existing + ' form-control').strip()
                widget.attrs.update({'class': classes})
            # Add a placeholder based on the field label if not already provided
            widget.attrs.setdefault('placeholder', field.label or '')

class CustomUserRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUserProfile
        fields = ['first_name', 'last_name', 'email']