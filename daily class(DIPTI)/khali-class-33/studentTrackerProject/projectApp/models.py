from django.db import models
from django.contrib.auth.models import AbstractUser

class customUserModel(AbstractUser):
    studentName = models.CharField(max_length=100, null=True)
    studentId = models.CharField(max_length=20, null=True)

class projectModel(models.Model):
    status = [
        ('NotStarted', 'Not Started'),
        ('InProgress', 'In Progress'),
        ('Completed', 'Completed'),
    ]
    user = models.ForeignKey(customUserModel, on_delete=models.CASCADE, null=True)
    projectName = models.CharField(max_length=100, null=True)
    projectDescription = models.TextField(null=True)
    projectStatus = models.CharField(max_length=20, choices=status, default='NotStarted', null=True)
    createdBy = models.CharField(max_length=100, null=True)
    createAt = models.DateTimeField(auto_now_add=True, null=True)
    updatedAt = models.DateTimeField(auto_now=True, null=True)