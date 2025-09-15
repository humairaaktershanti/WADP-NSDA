from django.db import models
from userAuthApp.models import *
from employerApp.models import *

class candidateProfileModel(models.Model):
    candidateUser = models.OneToOneField(customUserModel,on_delete=models.CASCADE, max_length = 100,null = True)
    fullName = models.CharField(max_length = 100,null = True)
    phone = models.CharField(max_length = 100,null=True)
    email = models.EmailField(null = True)
    address = models.CharField(max_length = 100, null = True)
    dateOfBirth = models.DateField(null = True)
    
class jobApplicatonModel(models.Model):
    job = models.OneToOneField(jobModel,on_delete=models.CASCADE, max_length = 100,null = True)
    candidate = models.OneToOneField(candidateProfileModel,on_delete=models.CASCADE, max_length = 100,null = True)
    lastEducation = models.CharField(max_length = 100,null = True)
    workExperience = models.CharField(max_length = 100,null = True)
    status = models.TextField(null = True)
    appliedAt = models.DateField(auto_now_add=True,null = True)

    

