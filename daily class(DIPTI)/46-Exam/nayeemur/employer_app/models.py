from django.db import models
from users_auth_app.models import CustomUserModel

class EmployerProfileModel(models.Model):
    employer_user=models.ForeignKey(CustomUserModel, on_delete=models.CASCADE)
    company_name=models.CharField(max_length=100)
    email=models.EmailField()
    phone=models.CharField(max_length=15)
    about_company=models.TextField() 
    company_logo=models.ImageField(upload_to='compamy_logo') 
    location=models.CharField(max_length=200)

    def _str_(self):
        return self.company_name
    


class JobModel(models.Model):
    JOB_TYPES=[
        ('Full-Time','Full-Time'),
        ('Remote','Remote'),
        ('Internship','Internship'),
    ]

    employer=models.ForeignKey(EmployerProfileModel,on_delete=models.CASCADE)
    title=models.CharField(max_length=100)
    description=models.TextField()
    requirements=models.TextField()
    salary=models.CharField(max_length=40)
    job_type=models.CharField(max_length=30, choices=JOB_TYPES)
    deadline=models.DateField()
    posted_date=models.DateField(auto_now_add=True)
