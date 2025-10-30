# registration/forms.py
from django import forms
from .models import CustomUserProfile
from .models import StallApplication
from django.contrib.auth.forms import UserCreationForm

class StallApplicationForm(forms.ModelForm):
    class Meta:
        model = StallApplication
        fields = ['stall_name', 'location', 'description', 'document']
class CustomUserRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUserProfile
        fields = ['first_name', 'last_name', 'email']