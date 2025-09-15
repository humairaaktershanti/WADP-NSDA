from django.db import models
from user_auth.models import *

# Create your models here.
class EmployerProfileModel(models.Model):
    employer_user = models.ForeignKey(customUserModel,null=True,on_delete=models.CASCADE)
    company_name=models.CharField(max_length=100,null=True)
    phone=models.CharField(max_length=100,null=True)
    about_company=models.CharField(max_length=100,null=True)
    company_logo=models.ImageField(null=True,upload_to='midea/image')
    location=models.CharField(max_length=100,null=True)

    def __str__(self):
        return self.employer_user


class jobModel(models.Model):
    emplayer=models.ForeignKey(EmployerProfileModel,on_delete=models.CASCADE,null=True)
    title=models.CharField(max_length=100,null=True)
    description=models.CharField(max_length=100,null=True)
    requirements=models.CharField(max_length=100,null=True)
    salary=models.IntegerField(null=True)
    job_type=models.CharField(max_length=100,null=True,choices=[
        ('Full_Time','Full_Time'),
        ('Remote','Remote'),
        ('Internship','Internship'),

    ])

    def __str__(self):
        return self.emplayer
    
    
