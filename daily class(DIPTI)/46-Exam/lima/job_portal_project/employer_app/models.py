from django.db import models
from users_auth_app.models import*

# Create your models here.

class EmployerProfileModel(models.Model):
    employer_user=models.OneToOneField(CustomUserModel , on_delete=models.CASCADE)
    company_name=models.CharField(max_length=100,null=True)
    phone=models.CharField(max_length=100,null=True)
    address=models.CharField(max_length=100,null=True)
    email=models.EmailField(null=True)
    date_of_birth=models.DateField(max_length=100,null=True)

class JobModel(models.Model):
    employer=models.OneToOneField(EmployerProfileModel,on_delete=models.CASCADE)
    title=models.CharField(max_length=100,null=True)
    description=models.CharField(max_length=100,null=True)
    requirements=models.CharField(max_length=100,null=True)
    salary=models.IntegerField(null=True)
   
    JOB_TYPE=[
       ('full_time','full_time'),
       ('remote','remote'),
       ('internship','internship')
   ]
    job_type=models.CharField(max_length=100,choices=JOB_TYPE)
    
