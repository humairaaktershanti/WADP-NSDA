from django import forms
from adminApp.models import PromotionModel, TerminationModel, User, ProfileModel, ResignationModel


class ProfileForm(forms.ModelForm):
    class Meta:
        model = ProfileModel
        fields = [
            'employee_id', 'full_name', 'position', 'phone', 'address',
            'birthday', 'gender', 'date_of_joining', 'profile_image', 'reports_to'
        ]
        widgets = {
            'employee_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Employee ID'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'position': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Position'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Address', 'rows': 2}),
            'birthday': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'Birthday'}),
            'gender': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Gender'}),
            'date_of_joining': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'Date of Joining'}),
            'profile_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'reports_to': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Reports To'}),
        }

class PromotionModelForm(forms.ModelForm):
    class Meta:
        model = PromotionModel
        fields = ['employee', 'department', 'designation_from', 'designation_to', 'promotion_date']
        widgets = {
            'promotion_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'employee': forms.Select(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'designation_from': forms.Select(attrs={'class': 'form-control'}),
            'designation_to': forms.Select(attrs={'class': 'form-control'}),
        }

class ResignationModelForm(forms.ModelForm):
    class Meta:
        model = ResignationModel
        fields = ['reason', 'resignation_date'] 
        widgets = {
            'resignation_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

class TerminationModelForm(forms.ModelForm):
    class Meta:
        model = TerminationModel
        fields = ['employee', 'department', 'termination_type', 'termination_date', 'notice_date', 'reason']
        widgets = {
            'termination_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'notice_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'employee': forms.Select(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'termination_type': forms.Select(attrs={'class': 'form-control'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['full_name', 'email', 'role', 'avatar']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }