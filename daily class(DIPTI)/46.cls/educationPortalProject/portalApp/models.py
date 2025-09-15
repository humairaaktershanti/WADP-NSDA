from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    userType = models.CharField(max_length=20, choices=[
        ('Admin', 'Admin'),
        ('Teacher', 'Teacher'),
    ],null=True)

class TeacherModel(models.Model):
    name= models.CharField(max_length=100,null=True)
    email = models.EmailField(null=True)
    phone = models.CharField(max_length=15, null=True)
    address= models.TextField(null=True)

    def __str__(self):
        return self.name

class StudentBasicInModel(models.Model):
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(null=True)
    address = models.TextField(null=True)

    def __str__(self):
        return self.name
    
class StudentEducationInfoModel(models.Model):
    student = models.ForeignKey(StudentBasicInModel, on_delete=models.CASCADE)
    degreeName = models.CharField(max_length=100, null=True)
    grade = models.CharField(max_length=10, null=True)
    year_of_passing = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.student.name} - {self.degreeName}"    
    
    

