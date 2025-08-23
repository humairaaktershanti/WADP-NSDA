from django import forms
from .models import Enrollment, LeaveApplication, FeePayment

class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['status', 'fee_paid']

class LeaveApplicationForm(forms.ModelForm):
    class Meta:
        model = LeaveApplication
        fields = ['start_date', 'end_date', 'reason']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

class FeePaymentForm(forms.ModelForm):
    class Meta:
        model = FeePayment
        fields = ['amount', 'payment_method', 'transaction_id', 'for_month']
        widgets = {
            'for_month': forms.DateInput(attrs={'type': 'month'}),
        }