from django.db import models
from user_auth_app.models import *


class EmployerProfileModel(models.Model):
    employer_user = models.OneToOneField(CustomUserModel,on_delete=models.CASCADE, null=True)
       
    company_name = models.CharField(max_length=255, null=True)
    email = models.EmailField(null=True)
    phone = models.CharField(max_length=15, null=True)
    about_company = models.TextField(null=True, blank=True)
    company_logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    location = models.CharField(max_length=255,null=True, blank=True)

    def __str__(self):
        return f"{self.company_name} ({self.employer_user.username})"
    

class JobModel(models.Model):
    JOB_TYPE_CHOICES = [
        ('Full-Time', 'Full-Time'),
        ('Remote', 'Remote'),
        ('Internship', 'Internship'),
    ]

    employer = models.ForeignKey(EmployerProfileModel,on_delete=models.CASCADE,related_name='job_posts')
    title = models.CharField(max_length=255,null= True)
    description = models.CharField(max_length=150, null= True)
    requirements = models.CharField(max_length=130, null= True)
    salary = models.IntegerField(null= True)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, null=True)
    deadline = models.DateField(null=True)
    posted_date = models.DateField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.title} at {self.employer.company_name}"
