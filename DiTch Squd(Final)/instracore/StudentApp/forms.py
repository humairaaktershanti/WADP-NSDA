from django import forms
from StudentApp.models import Enrollment, Certificate

class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['course']
        widgets = {
            'course': forms.Select(attrs={'class': 'form-select'})
        }

class CertificateApplicationForm(forms.ModelForm):
    class Meta:
        model = Certificate
        fields = ['certificate_type']
        widgets = {
            'certificate_type': forms.Select(attrs={'class': 'form-select'})
        }