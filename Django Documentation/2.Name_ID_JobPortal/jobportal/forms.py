from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile, RecruiterProfile, JobSeekerProfile, JobPost, Application

class UserRegistrationForm(UserCreationForm):
    display_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    user_type = forms.ChoiceField(choices=UserProfile.USER_TYPES)
    
    class Meta:
        model = User
        fields = ['username', 'display_name', 'email', 'user_type', 'password1', 'password2']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['display_name', 'phone']

class RecruiterProfileForm(forms.ModelForm):
    class Meta:
        model = RecruiterProfile
        fields = ['company_name', 'company_description', 'company_website', 'company_location']

class JobSeekerProfileForm(forms.ModelForm):
    class Meta:
        model = JobSeekerProfile
        fields = ['skills', 'experience', 'education']
        widgets = {
            'skills': forms.Textarea(attrs={'rows': 3}),
            'experience': forms.Textarea(attrs={'rows': 4}),
            'education': forms.Textarea(attrs={'rows': 4}),
        }

class ResumeUploadForm(forms.ModelForm):
    class Meta:
        model = JobSeekerProfile
        fields = ['resume']

class JobPostForm(forms.ModelForm):
    class Meta:
        model = JobPost
        fields = ['title', 'description', 'category', 'required_skills', 'number_of_openings', 
                 'location', 'salary_min', 'salary_max', 'last_date_to_apply']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'required_skills': forms.Textarea(attrs={'rows': 3}),
            'last_date_to_apply': forms.DateInput(attrs={'type': 'date'}),
        }

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['cover_letter']
        widgets = {
            'cover_letter': forms.Textarea(attrs={'rows': 5}),
        }