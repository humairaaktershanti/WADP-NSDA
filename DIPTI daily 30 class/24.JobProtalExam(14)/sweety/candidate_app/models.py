from django.db import models
from user_auth.models import *
from employer_app.models import *

# Create your models here.
class CandidateProfileModel(models.Model):
    candidate_user = models.ForeignKey(customUserModel, null=True, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=100, null=True)
    email = models.EmailField(null=True)
    address = models.CharField(max_length=100, null=True)
    dath_of_birth = models.DateField(null=True)
    def __str__(self):
        return self.full_name
    

class  jobApplicationModel(models.Model):
    candidate = models.ForeignKey(CandidateProfileModel, on_delete=models.CASCADE, null=True)
    job = models.ForeignKey(jobModel, on_delete=models.CASCADE, null=True)
    last_education = models.CharField(max_length=100, null=True)
    wark_experience = models.CharField(max_length=100, null=True)
    status = models.CharField(max_length=100, null=True, choices=[
        ('applied', 'applied'),
        ('interview', 'interview'),
        ('offered', 'offered'),
        ('rejected', 'rejected'),
    ])
    applied_at = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return self.job