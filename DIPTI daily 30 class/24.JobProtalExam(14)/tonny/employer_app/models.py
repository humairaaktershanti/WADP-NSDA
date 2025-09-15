from django.db import models
from users_auth_app.models import *

class EmployerProfileModel(models.Model):

    employer_user=models.ForeignKey(CustomUserModel, on_delete=models.CASCADE, null=True)
    company_name=models.CharField(max_length=250, null=True)
    email=models.EmailField(null=True)
    phone=models.CharField(max_length=50, null=True)
    about_company=models.CharField(max_length=250, null=True)
    company_logo=models.ImageField(upload_to='media/image', null=True)
    location=models.CharField(max_length=250, null=True)
    
    def __str__(self):
        return self.company_name
    
    
class JobModel(models.Model):
    
    employer=models.ForeignKey(EmployerProfileModel, on_delete=models.CASCADE, null=True)
    username=models.CharField(max_length=50, null=True)
 
    job_type=models.CharField(choices=[
        ('Full_Time', 'Full_Time'),
        ('Remote', 'Remote'),
        ('Internship', 'Internship'),
    ], max_length=100, null=True)
        
    title=models.CharField(max_length=150, null=True)
    description=models.TextField(null=True)
    requirements=models.CharField(max_length=250, null=True) 
    salary=models.CharField(max_length=150, null=True)
    deadline=models.DateField(auto_now=True, null=True)
    posted_date=models.DateField(auto_now=True, null=True) 
      
    def __str__(self):
        return self.title