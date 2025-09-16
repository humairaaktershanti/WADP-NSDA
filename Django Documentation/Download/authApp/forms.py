from django import forms
from .models import Profile, oneModel, TwoModel

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'location', 'birth_date']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'})
        }

class oneForm(forms.ModelForm):
    class Meta:
        model = oneModel
        fields = ['itemName', 'cunt', 'totalItems']

class twoForm(forms.ModelForm):
    class Meta:
        model = TwoModel
        fields = '__all__'