from django.db import models
from AuthApp.models import User
from EmployeeApp.models import Course

class Enrollment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('dropped', 'Dropped'),
    ]
    
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="enrollments")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="enrollments")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    fee_paid = models.BooleanField(default=False)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    progress_percentage = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student.username} - {self.course.title}"

class ExamResult(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name="results")
    exam_name = models.CharField(max_length=200)
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2)
    total_marks = models.DecimalField(max_digits=5, decimal_places=2)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    grade = models.CharField(max_length=5, blank=True)
    passed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    remarks = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if self.total_marks > 0:
            self.percentage = (self.marks_obtained / self.total_marks) * 100
            
            # Determine grade
            if self.percentage >= 90:
                self.grade = 'A+'
            elif self.percentage >= 80:
                self.grade = 'A'
            elif self.percentage >= 70:
                self.grade = 'B+'
            elif self.percentage >= 60:
                self.grade = 'B'
            elif self.percentage >= 50:
                self.grade = 'C'
            else:
                self.grade = 'F'
            
            # Determine if passed
            self.passed = self.percentage >= 50
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.enrollment.student.username} - {self.exam_name} - {self.grade}"

class Certificate(models.Model):
    TYPE_CHOICES = [
        ('online', 'Online Course'),
        ('regular', 'Regular Course'),
        ('diploma', 'Diploma'),
    ]
    
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="certificates")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="certificates")
    certificate_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    issue_date = models.DateField(auto_now_add=True)
    expiry_date = models.DateField(null=True, blank=True)
    certificate_number = models.CharField(max_length=50, unique=True)
    verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    pdf_file = models.FileField(upload_to="certificates/", blank=True, null=True)

    def __str__(self):
        return f"{self.student.username} - {self.course.title} Certificate"

class GuardianReport(models.Model):
    REPORT_TYPE_CHOICES = [
        ('monthly', 'Monthly Report'),
        ('results', 'Results Report'),
        ('attendance', 'Attendance Report'),
        ('payment', 'Payment Report'),
        ('other', 'Other'),
    ]
    
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="guardian_reports")
    report_type = models.CharField(max_length=50, choices=REPORT_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    sent_to = models.EmailField()  # Guardian's email
    is_sent = models.BooleanField(default=False)
    sent_method = models.CharField(max_length=20, default="email")  # email, sms

    def __str__(self):
        return f"{self.title} for {self.student.username}"

class LeaveApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="leave_applications")
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    applied_at = models.DateTimeField(auto_now_add=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="approved_leaves")
    approved_at = models.DateTimeField(null=True, blank=True)
    remarks = models.TextField(blank=True)

    def __str__(self):
        return f"{self.student.username} - {self.start_date} to {self.end_date}"

class FeePayment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('bank_transfer', 'Bank Transfer'),
        ('online', 'Online Payment'),
        ('check', 'Check'),
    ]
    
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="fee_payments")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    transaction_id = models.CharField(max_length=100, blank=True)
    payment_date = models.DateField(auto_now_add=True)
    for_month = models.DateField()  # Only month and year are used
    is_verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="verified_payments")
    verified_at = models.DateTimeField(null=True, blank=True)
    remarks = models.TextField(blank=True)

    def __str__(self):
        return f"{self.student.username} - {self.amount} for {self.for_month.strftime('%B %Y')}"