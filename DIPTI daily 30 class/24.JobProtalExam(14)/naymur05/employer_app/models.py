from django.db import models
from user_auth_app.models import CustomUserModel

class EmployerProfileModel(models.Model):
    employer_user=models.OneToOneField(CustomUserModel, on_delete=models.CASCADE, related_name='employer_profile')
    company_name = models.CharField(max_length=255)
    email= models.EmailField(blank=True, null=True)
    phone= models.CharField(max_length=15, blank=True, null=True)
    about_company = models.TextField(blank=True, null=True)
    company_logo = models.ImageField(upload_to='Media/company_logos', blank=True, null=True)
    location = models.TextField(blank=True, null=True)

class jobModel(models.Model):
    employer = models.ForeignKey(EmployerProfileModel, on_delete=models.CASCADE, related_name='jobs')
    title = models.CharField(max_length=255)
    description = models.TextField()
    requirements = models.TextField(blank=True, null=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    job_type = models.CharField(max_length=50, choices=[('full_time', 'Full Time'), ('remote', 'Remote'), ('internship', 'Internship')])
    deadline = models.DateField()
    posted_date = models.DateTimeField(auto_now_add=True)




