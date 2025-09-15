from django import forms
from .models import Profile, Contact

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'skills', 'experience', 'education', 'profile_image', 'contact_email', 'phone_number', 'github_url', 'linkedin_url']

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'