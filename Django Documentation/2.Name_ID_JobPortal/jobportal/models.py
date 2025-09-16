from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

class UserProfile(models.Model):
    USER_TYPES = (
        ('jobseeker', 'Job Seeker'),
        ('recruiter', 'Recruiter'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=USER_TYPES)
    display_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.user.username

class RecruiterProfile(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=200)
    company_description = models.TextField(blank=True, null=True)
    company_website = models.URLField(blank=True, null=True)
    company_location = models.CharField(max_length=200, blank=True, null=True)
    
    def __str__(self):
        return self.company_name

class JobSeekerProfile(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    skills = models.TextField(help_text="Enter your skills separated by commas")
    resume = models.FileField(
        upload_to='resumes/', 
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx'])],
        blank=True, null=True
    )
    experience = models.TextField(blank=True, null=True)
    education = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.user_profile.display_name

class JobPost(models.Model):
    JOB_CATEGORIES = (
        ('IT', 'Information Technology'),
        ('Finance', 'Finance'),
        ('Healthcare', 'Healthcare'),
        ('Education', 'Education'),
        ('Marketing', 'Marketing'),
        ('Other', 'Other'),
    )
    
    recruiter = models.ForeignKey(RecruiterProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=JOB_CATEGORIES)
    required_skills = models.TextField(help_text="Enter required skills separated by commas")
    number_of_openings = models.PositiveIntegerField(default=1)
    location = models.CharField(max_length=200)
    salary_min = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    salary_max = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    posted_date = models.DateTimeField(auto_now_add=True)
    last_date_to_apply = models.DateField()
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title

class Application(models.Model):
    APPLICATION_STATUS = (
        ('applied', 'Applied'),
        ('under_review', 'Under Review'),
        ('shortlisted', 'Shortlisted'),
        ('rejected', 'Rejected'),
        ('hired', 'Hired'),
    )
    
    job_post = models.ForeignKey(JobPost, on_delete=models.CASCADE)
    job_seeker = models.ForeignKey(JobSeekerProfile, on_delete=models.CASCADE)
    applied_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=APPLICATION_STATUS, default='applied')
    cover_letter = models.TextField(blank=True, null=True)
    
    class Meta:
        unique_together = ('job_post', 'job_seeker')
    
    def __str__(self):
        return f"{self.job_seeker.user_profile.display_name} - {self.job_post.title}"