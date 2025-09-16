from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile, ConsumedCalorie

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name', 'age', 'gender', 'height', 'weight']
        widgets = {
            'age': forms.NumberInput(attrs={'min': 1, 'max': 120}),
            'height': forms.NumberInput(attrs={'step': 0.1, 'min': 50, 'max': 250}),
            'weight': forms.NumberInput(attrs={'step': 0.1, 'min': 20, 'max': 300}),
        }

class ConsumedCalorieForm(forms.ModelForm):
    class Meta:
        model = ConsumedCalorie
        fields = ['item_name', 'calories']
        widgets = {
            'calories': forms.NumberInput(attrs={'step': 0.1, 'min': 0}),
        }

class CalorieGoalForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['daily_calorie_goal']
        widgets = {
            'daily_calorie_goal': forms.NumberInput(attrs={'step': 0.1, 'min': 0}),
        }