from django.db import models

# Create your models here.
class candidateModel(models.Model):
    full_name=models.CharField(max_length=50,null=True)
    email=models.CharField(max_length=50)
    phone_number=models.CharField(max_length=50)
    address=models.CharField(max_length=50)
    job_title=models.CharField(max_length=50)
    linkedin_profile=models.CharField(max_length=50)
    university=models.CharField(max_length=50)
    degree=models.CharField(max_length=50)
    languages=models.CharField(max_length=50)
    years_of_experience=models.CharField(max_length=50)