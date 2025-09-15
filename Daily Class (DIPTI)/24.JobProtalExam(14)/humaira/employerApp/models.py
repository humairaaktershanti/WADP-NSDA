from django.db import models
from userAuthApp.models import *

class employerProfileModel(models.Model):
    employerUser = models.OneToOneField(customUserModel,on_delete=models.CASCADE, max_length = 100,null = True)
    companyName = models.CharField(max_length = 100,null = True)
    email = models.EmailField(null = True)
    phone = models.IntegerField(null=True)
    aboutCompany = models.CharField(max_length = 100,null = True)
    companyLogo = models.ImageField(upload_to='media/photo', null = True)
    location = models.CharField(max_length = 100,null = True)
    
    
class jobModel(models.Model):
    employer = models.OneToOneField(employerProfileModel,on_delete=models.CASCADE, max_length = 100,null = True)
    title = models.TimeField(null = True)
    description = models.TextField(null = True)
    salary = models.PositiveIntegerField(null=True)
    jobType = models.CharField(max_length = 100,null = True)
    deadline = models.DateField(null = True)
    postedDate = models.DateField(auto_now_add=True,null = True)
    

