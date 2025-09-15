from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class customUser(AbstractUser):
    userType=models.CharField(max_length=100,choices=[
        ('Admin','Admin'),
        ('Teacher','Teacher'),
        ('Student','Student'),
    ],null=True)

class teacherModel(models.Model):
    user=models.OneToOneField(customUser,on_delete=models.CASCADE,null=True)
    teacherName=models.CharField(max_length=100,null=True)
    phoneNumber=models.CharField(max_length=19,null=True)
    profileImage=models.ImageField(upload_to="media/photo",null=True)

class studentModel(models.Model):
    user=models.OneToOneField(customUser,on_delete=models.CASCADE,null=True)
    studentName=models.CharField(max_length=100,null=True)
    phoneNumber=models.CharField(max_length=19,null=True)
    profileImage=models.ImageField(upload_to="media/photo",null=True)

class studentPendingModel(models.Model):
    username = models.CharField(max_length=150,null=True)
    email = models.EmailField(blank=True, null=True)
    userType=models.CharField(max_length=100,choices=[
        ('Student','Student'),
    ],null=True)
    studentName=models.CharField(max_length=100,null=True)
    phoneNumber=models.CharField(max_length=19,null=True)
    profileImage=models.ImageField(upload_to="media/photo",null=True)