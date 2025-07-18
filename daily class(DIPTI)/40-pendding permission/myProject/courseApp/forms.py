from django import forms
from courseApp.models import *

class addCourseForms(forms.ModelForm):
    class Meta:
        model = courseModel
        fields=['courseTitle','courseDescription','courseDuration','courseStartDate','courseFee']

class addAdmittedForms(forms.ModelForm):
    class Meta:
        model = admittedModel
        fields=['payment','due']





    