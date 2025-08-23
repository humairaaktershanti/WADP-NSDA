from django import forms
from .models import (
    JobPost, Application, InterviewSchedule,
    Salary, Expense, Transaction,
    Course, Assignment, LessonPlan, Attendance
)

class JobPostForm(forms.ModelForm):
    class Meta:
        model = JobPost
        fields = ['title', 'description', 'requirements', 'is_active']

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['applicant_name', 'applicant_email', 'applicant_phone', 'resume', 'cover_letter']

class InterviewScheduleForm(forms.ModelForm):
    class Meta:
        model = InterviewSchedule
        fields = ['application', 'scheduled_date', 'location', 'interview_type', 'notes']
        widgets = {
            'scheduled_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class SalaryForm(forms.ModelForm):
    class Meta:
        model = Salary
        fields = ['employee', 'amount', 'month', 'status', 'notes']
        widgets = {
            'month': forms.DateInput(attrs={'type': 'month'}),
        }

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['category', 'amount', 'description', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['user', 'amount', 'transaction_type', 'description', 'reference_id']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'course_type', 'price', 'duration_weeks', 
                 'status', 'start_date', 'end_date', 'syllabus']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['course', 'title', 'description', 'due_date', 'total_marks']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }

class LessonPlanForm(forms.ModelForm):
    class Meta:
        model = LessonPlan
        fields = ['course', 'title', 'content', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['user', 'attendee_type', 'date', 'status', 'course', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }