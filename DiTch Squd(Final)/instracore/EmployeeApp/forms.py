# EmployeeApp/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.utils import timezone
from .models import JobPost, Application, InterviewSchedule, Course, CourseTeacher, Assignment, LessonPlan, ClassRoutine, Attendance
from AuthApp.models import User

class UserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'role', 'sub_role')
        
class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'role', 'sub_role', 'is_active', 'date_of_birth', 'phone', 'gender', 'location', 'country')

class JobPostForm(forms.ModelForm):
    class Meta:
        model = JobPost
        fields = ('title', 'description', 'role', 'min_requirements', 'salary_range', 'location', 'language', 'availability', 'application_instructions', 'deadline')
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'})
        }

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ('applicant_name', 'applicant_email', 'status', 'resume', 'cover_letter')

class InterviewScheduleForm(forms.ModelForm):
    class Meta:
        model = InterviewSchedule
        fields = ('scheduled_date', 'interviewer', 'notes', 'status', 'feedback')
        widgets = {
            'scheduled_date': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter interviewers to only show HR users
        self.fields['interviewer'].queryset = User.objects.filter(role='employee', sub_role='hr')

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('title', 'description', 'course_type', 'price', 'duration', 'status', 'syllabus')

class CourseTeacherForm(forms.ModelForm):
    class Meta:
        model = CourseTeacher
        fields = ('course', 'teacher', 'is_primary')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter teachers to only show teacher users
        self.fields['teacher'].queryset = User.objects.filter(role='employee', sub_role='teacher')

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ('course', 'title', 'description', 'due_date', 'total_marks', 'is_active')
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'})
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        # Filter courses to only show courses taught by this teacher
        if self.user and self.user.sub_role == 'teacher':
            self.fields['course'].queryset = Course.objects.filter(teachers__teacher=self.user)

class LessonPlanForm(forms.ModelForm):
    class Meta:
        model = LessonPlan
        fields = ('course', 'title', 'content', 'date')
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        # Filter courses to only show courses taught by this teacher
        if self.user and self.user.sub_role == 'teacher':
            self.fields['course'].queryset = Course.objects.filter(teachers__teacher=self.user)

class ClassRoutineForm(forms.ModelForm):
    class Meta:
        model = ClassRoutine
        fields = ('course', 'day_of_week', 'start_time', 'end_time', 'room', 'is_active')
        widgets = {
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'})
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        # Filter courses to only show courses taught by this teacher
        if self.user and self.user.sub_role == 'teacher':
            self.fields['course'].queryset = Course.objects.filter(teachers__teacher=self.user)

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ('user', 'date', 'status', 'check_in_time', 'check_out_time', 'notes')
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'check_in_time': forms.TimeInput(attrs={'type': 'time'}),
            'check_out_time': forms.TimeInput(attrs={'type': 'time'})
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        # Filter users to only show students enrolled in courses taught by this teacher
        if self.user and self.user.sub_role == 'teacher':
            from StudentApp.models import Enrollment
            student_ids = Enrollment.objects.filter(
                course__teachers__teacher=self.user
            ).values_list('student_id', flat=True)
            self.fields['user'].queryset = User.objects.filter(id__in=student_ids)

# Filter forms for modals
class UserFilterForm(forms.Form):
    role = forms.ChoiceField(required=False, choices=[
        ('', 'All Roles'),
        ('employee', 'Employee'),
        ('candidate', 'Candidate'),
        ('student', 'Student'),
    ])
    sub_role = forms.ChoiceField(required=False, choices=[
        ('', 'All Sub Roles'),
        ('faculty', 'Faculty'),
        ('hr', 'HR'),
        ('finance', 'Finance'),
        ('marketing', 'Marketing'),
        ('it', 'IT'),
        ('teacher', 'Teacher'),
        ('other', 'Other'),
    ])
    search = forms.CharField(required=False, max_length=100)

class JobPostFilterForm(forms.Form):
    search = forms.CharField(required=False, max_length=100)
    is_active = forms.ChoiceField(required=False, choices=[
        ('', 'All Statuses'),
        ('1', 'Active'),
        ('0', 'Inactive'),
    ])

class ApplicationFilterForm(forms.Form):
    job = forms.ModelChoiceField(required=False, queryset=JobPost.objects.all(), empty_label="All Jobs")
    status = forms.ChoiceField(required=False, choices=[
        ('', 'All Statuses'),
        ('pending', 'Pending'),
        ('under_review', 'Under Review'),
        ('interview_scheduled', 'Interview Scheduled'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('hired', 'Hired'),
    ])

class InterviewFilterForm(forms.Form):
    status = forms.ChoiceField(required=False, choices=[
        ('', 'All Statuses'),
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ])
    search = forms.CharField(required=False, max_length=100)

class CourseFilterForm(forms.Form):
    course_type = forms.ChoiceField(required=False, choices=[
        ('', 'All Types'),
        ('online', 'Online'),
        ('regular', 'Regular'),
        ('diploma', 'Diploma'),
        ('offline', 'Offline'),
    ])
    status = forms.ChoiceField(required=False, choices=[
        ('', 'All Statuses'),
        ('draft', 'Draft'),
        ('pending_approval', 'Pending Approval'),
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('closed', 'Closed'),
    ])
    search = forms.CharField(required=False, max_length=100)

class AssignmentFilterForm(forms.Form):
    course = forms.ModelChoiceField(required=False, queryset=Course.objects.all(), empty_label="All Courses")
    is_active = forms.ChoiceField(required=False, choices=[
        ('', 'All Statuses'),
        ('1', 'Active'),
        ('0', 'Inactive'),
    ])

class LessonPlanFilterForm(forms.Form):
    course = forms.ModelChoiceField(required=False, queryset=Course.objects.all(), empty_label="All Courses")
    month = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'month'}))

class ClassRoutineFilterForm(forms.Form):
    course = forms.ModelChoiceField(required=False, queryset=Course.objects.all(), empty_label="All Courses")
    day_of_week = forms.ChoiceField(required=False, choices=[
        ('', 'All Days'),
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    ])

class AttendanceFilterForm(forms.Form):
    course = forms.ModelChoiceField(required=False, queryset=Course.objects.all(), empty_label="All Courses")
    date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    status = forms.ChoiceField(required=False, choices=[
        ('', 'All Statuses'),
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('leave', 'On Leave'),
        ('late', 'Late'),
    ])