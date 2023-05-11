from django import forms
from .models import Profile
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_pic','first_name','username','email','bio']
