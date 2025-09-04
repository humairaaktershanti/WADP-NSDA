from django.db import models

# Create your models here.
class resumeInfoModel(models.Model):
    ProfileImage=models.ImageField(upload_to='static/image/', null=True)
    FullName=models.CharField(max_length=50, null=True)
    Address=models.CharField(max_length=50, null=True)
    PhoneNumber=models.CharField(max_length=50, null=True)
    EmailAddress=models.CharField(max_length=50, null=True)
    CareerObjective=models.TextField()
    Skills=models.CharField(max_length=50, null=True)
    Certifications=models.CharField(max_length=50, null=True)
    Projects=models.CharField(max_length=50, null=True)
    References=models.CharField(max_length=50, null=True)

class educationModel(models.Model):
    FullName=models.CharField(max_length=50, null=True)
    Degree=models.CharField(max_length=50, null=True)
    institute=models.CharField(max_length=50, null=True)
    graduation=models.CharField(max_length=50, null=True)

class workModel(models.Model):
    FullName=models.CharField(max_length=50, null=True)
    Company=models.CharField(max_length=50, null=True)
    Position=models.CharField(max_length=50, null=True)
    StartDate=models.CharField(max_length=50, null=True)
    EndDate=models.CharField(max_length=50, null=True)