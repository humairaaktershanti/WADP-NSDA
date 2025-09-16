from django import forms
from employeeApp.models import *

class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model = LeaveRequestModel
        fields = ["leave_type", "start_date", "end_date", "reason"]
        widgets = {
            'leave_type': forms.Select(attrs={'class': 'form-select'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = AttendanceModel
        fields = ['date', 'status', 'check_in', 'check_out', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'check_in': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'check_out': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }


class TaskForm(forms.ModelForm):
    class Meta:
        model = TaskModel
        fields = ['title', 'description', 'assigned_to', 'department', 'designation', 'status', 'due_date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter task title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Enter task description'}),
            'assigned_to': forms.Select(attrs={'class': 'form-select'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'designation': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            leader_teams = TeamMemberModel.objects.filter(member=user.profile, role='Lead').values_list('team', flat=True)
            self.fields['assigned_to'].queryset = ProfileModel.objects.filter(teams__team__in=leader_teams)
        self.fields['status'].initial = 'pending'

class TaskStatusForm(forms.ModelForm):
    class Meta:
        model = TaskModel
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
        }


class TeamForm(forms.ModelForm):
    class Meta:
        model = TeamModel
        fields = ["name", "department", "description"]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter team name'
            }),
            'department': forms.Select(attrs={
                'class': 'form-select'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter team description',
                'rows': 3
            }),
        }


class TeamMemberForm(forms.ModelForm):
    class Meta:
        model = TeamMemberModel
        fields = ["member", "role"]
        widgets = {
            'team': forms.Select(attrs={
                'class': 'form-select'
            }),
            'member': forms.Select(attrs={
                'class': 'form-select'
            }),
            'role': forms.Select(attrs={
                'class': 'form-select'
            }),
        }
    def __init__(self, *args, **kwargs):
        team = kwargs.pop('team', None)
        super().__init__(*args, **kwargs)
        if team:
            # Only show users who are not already in this team
            self.fields['member'].queryset = ProfileModel.objects.exclude(teams__team=team)
        self.fields['member'].widget.attrs.update({'class': 'form-select'})
        self.fields['role'].widget.attrs.update({'class': 'form-select'})
        


