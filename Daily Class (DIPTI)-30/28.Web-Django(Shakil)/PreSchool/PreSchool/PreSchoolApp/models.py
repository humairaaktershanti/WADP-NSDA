from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class customeUser(AbstractUser):
    USERTYPE = [
        ('1','admin'),
        ('2','teacher'),
        ('3','student'),
    ]
    
    UserType = models.CharField(choices=USERTYPE,max_length=100)
    
class StudentModel(models.Model):
    user = models.OneToOneField(customeUser, on_delete =models.CASCADE,related_name='studentuser')
    FullName = models.CharField(max_length=100)
    StudentID = models.CharField(max_length=100)
    
    GENDER  = [
        ('male','Male'),
        ('female','Female'),
    ]
    Gender = models.CharField(choices=GENDER,max_length=100)
    DateOB = models.DateField(max_length=100)
    Religion = models.CharField(max_length=100)
    Mobile = models.CharField(max_length=100)
    StudentImage = models.ImageField(upload_to='static/studentimg/')
    PresentAddress = models.CharField(max_length=100)
    PermanentAddress = models.CharField(max_length=100)
    
    Department = models.CharField(max_length=100)
    StartSession = models.CharField(max_length=100)
    EndSession = models.CharField(max_length=100)
    Section = models.CharField(max_length=100)
    
    FatherName = models.CharField(max_length=100)
    FatherOccupation = models.CharField(max_length=100)
    FatherMobile = models.CharField(max_length=100)
    
    MotherName = models.CharField(max_length=100)
    MotherOccupation = models.CharField(max_length=100)
    MotherMobile = models.CharField(max_length=100)
    
    create_at = models.DateField(auto_now=True)
    update_at = models.DateField(auto_now_add=True)
    
    
    
class DepartmentModel(models.Model):
    department_name = models.CharField(max_length=100)
    department_head_name = models.CharField(max_length=100)
    create_at = models.DateField(auto_now=True)
    update_at = models.DateField(auto_now_add=True)
    
class SessionYearModel(models.Model):
    StartSession = models.CharField(max_length=100)
    EndSession = models.CharField(max_length=100)
    create_at = models.DateField(auto_now=True)
    update_at = models.DateField(auto_now_add=True)
    
    