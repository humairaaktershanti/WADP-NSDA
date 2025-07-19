from django.db import models
from django.contrib.auth.models import candidate_app
# Create your models here.
class CandidateProfileModel(models.Model):
    candidate_user= models.ForeignKey(CustomUserModel, on_delete=models.CASCADE, related_name='candidate_profile')
    full_name= models.CharField(max_length=100, null=True)
    email = models.EmailField(null=True)
    phone = models.CharField(max_length=15, null=True)
    address = models.CharField(max_length=100, null=True)
    data_of_birth = models.DateField(null=True)


class JobApplicationModel(models.Model):
    status=(
        ('Applied'= 'Applied'),
        ('Interview', 'Interview'),
        ('Offered', 'Offered'),
        ('Rejected', 'Rejected'),
    )
