from django import forms
from myApp.models import *
class studentForm(forms.ModelForm):
    class Meta:
        model = studentModel
        fields = '__all__'