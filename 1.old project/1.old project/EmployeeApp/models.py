from django.db import models
from AuthApp.models import User

# -------------------------
# HR MODELS
# -------------------------
class JobPost(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    requirements = models.TextField(blank=True)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="job_posts")
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Application(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('interview_scheduled', 'Interview Scheduled'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE, related_name="applications")
    applicant_name = models.CharField(max_length=200)
    applicant_email = models.EmailField()
    applicant_phone = models.CharField(max_length=20, blank=True)
    resume = models.FileField(upload_to="resumes/", blank=True, null=True)
    cover_letter = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    applied_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.applicant_name} - {self.job.title}"

class InterviewSchedule(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name="interviews")
    scheduled_date = models.DateTimeField()
    location = models.CharField(max_length=200, blank=True)
    interview_type = models.CharField(max_length=50, default="In-person")  # In-person, Video call, Phone
    notes = models.TextField(blank=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Interview for {self.application.applicant_name} on {self.scheduled_date}"

# -------------------------
# FINANCE MODELS
# -------------------------
class Salary(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('paid', 'Paid'),
        ('rejected', 'Rejected'),
    ]
    
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="salaries")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    month = models.DateField()  # Only month and year are used
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="approved_salaries")
    approved_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.employee.username} - {self.month.strftime('%B %Y')} - {self.amount}"

class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('utilities', 'Utilities'),
        ('maintenance', 'Maintenance'),
        ('supplies', 'Supplies'),
        ('marketing', 'Marketing'),
        ('travel', 'Travel'),
        ('other', 'Other'),
    ]
    
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    date = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="expenses")
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="approved_expenses")
    approved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.category} - {self.amount} on {self.date}"

class Transaction(models.Model):
    TYPE_CHOICES = [
        ('fee', 'Fee Payment'),
        ('salary', 'Salary Payment'),
        ('expense', 'Expense'),
        ('purchase', 'Purchase'),
        ('refund', 'Refund'),
        ('other', 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transactions")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    description = models.TextField(blank=True)
    date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    reference_id = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.transaction_type} - {self.amount}"

# -------------------------
# FACULTY / TEACHER MODELS
# -------------------------
class Course(models.Model):
    TYPE_CHOICES = [
        ('online', 'Online'),
        ('regular', 'Regular'),
        ('diploma', 'Diploma'),
        ('offline', 'Offline'),
    ]
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('closed', 'Closed'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    course_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    duration_weeks = models.PositiveIntegerField(default=4)
    assigned_teachers = models.ManyToManyField(User, related_name="courses", blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_courses")
    created_at = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    syllabus = models.TextField(blank=True)
    is_approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="approved_courses")
    approved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title

class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="assignments")
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateField()
    total_marks = models.DecimalField(max_digits=5, decimal_places=2, default=100)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_assignments")

    def __str__(self):
        return f"{self.title} - {self.course.title}"

class LessonPlan(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lesson_plans")
    title = models.CharField(max_length=200)
    content = models.TextField()
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_lesson_plans")

    def __str__(self):
        return f"{self.title} - {self.course.title}"

class Attendance(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('leave', 'Leave'),
        ('late', 'Late'),
    ]
    ATTENDEE_TYPE = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('staff', 'Staff'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    attendee_type = models.CharField(max_length=20, choices=ATTENDEE_TYPE)
    date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="present")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="attendances", blank=True, null=True)
    marked_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="marked_attendances")
    marked_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ('user', 'date', 'course')

    def __str__(self):
        return f"{self.user.username} - {self.status} on {self.date}"