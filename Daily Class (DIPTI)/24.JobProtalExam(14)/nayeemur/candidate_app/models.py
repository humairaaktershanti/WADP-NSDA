from django.db import models
from users_auth_app.models import *
from employer_app.models import *

class CandidateProfileModel:
    candidate_user=models.ForeignKey(CustomUserModel,on_delete=models.CASCADE)
    full_name=models.CharField(max_length=100)
    phone=models.CharField(max_length=15)
    email=models.EmailField()
    address=models.TextField()
    data_of_birth=models.DateField()

    def _str_ (self):
        return self.full_name
    

class JobApplicationModel(models.Model):
    JOB_STATUS=[
        ('Applied','Applied'),
        ('Interview','Interview'),
        ('Offered','Offered'),
        ('Rejected','Rejected'),
    ]
    job=models.ForeignKey(JobModel, on_delete=models.CASCADE)
    candidate=models.ForeignKey(CandidateProfileModel, on_delete=models.CASCADE)
    last_education=models.CharField(max_length=100)
    work_experience=models.TextField()
    status=models.CharField(max_length=30, choices=JOB_STATUS, default='Applied')
    applied_at=models.DateTimeField(auto_now_add=True)