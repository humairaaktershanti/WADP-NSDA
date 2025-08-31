from django import forms
from .models import *

class ProfileForm(forms.ModelForm):
    class Meta:
        model = ProfileModel
        fields = ['Name', 'Age', 'Gender', 'Height', 'Weight']
    