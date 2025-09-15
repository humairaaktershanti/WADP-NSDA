from django.db import models
from user_auth_app.models import CustomUserModel
from employer_app.models import jobModel


class CandidateProfileModel(models.Model):
    candidate_user = models.OneToOneField(CustomUserModel, on_delete=models.CASCADE, related_name='candidate_profile')
    full_name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address=models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

class jobApplicationModel(models.Model):
    candidate = models.ForeignKey(CandidateProfileModel, on_delete=models.CASCADE, related_name='application_name')
    job = models.ForeignKey(jobModel, on_delete=models.CASCADE, related_name='job_title')
    last_education = models.CharField(max_length=255, blank=True, null=True)
    work_experience = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=[('applied', 'Applied'), ('interview', 'Interview'), ('offered', 'Offered'), ('rejected', 'Rejected')], default='applied')
    applied_at = models.DateTimeField(auto_now_add=True)