from django.db import models
from users_auth_app.models import *
from employer_app.models import *

class CandidateProfileModel(models.Model):

    candidate_user=models.ForeignKey(CustomUserModel, on_delete=models.CASCADE, null=True)
    full_name=models.CharField(max_length=250, null=True)
    address=models.CharField(max_length=250, null=True)
    data_of_birth=models.DateField(auto_now=True, null=True)
    
    def __str__(self):
        return self.full_name
    
    
class JobApplicationModel(models.Model):
    
    job=models.ForeignKey(JobModel, on_delete=models.CASCADE, null=True)
    candidate=models.ForeignKey(CandidateProfileModel, on_delete=models.CASCADE, null=True)
    last_education=models.CharField(max_length=250, null=True)
    work_experience=models.CharField(max_length=250, null=True)
 
    status=models.CharField(choices=[
        ('Applied', 'Applied'),
        ('Interview', 'Interview'),
        ('Offered', 'Offered'),
        ('Rejected', 'Rejected'),
    ], max_length=100, null=True)
        
    applied_at=models.DateTimeField(auto_now_add=True, null=True) 
      
    def __str__(self):
        return self.candidate.full_name