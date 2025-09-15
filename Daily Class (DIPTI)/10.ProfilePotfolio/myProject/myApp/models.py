from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class customUser(AbstractUser):

    gender=models.CharField(choices=[
        ('male',"Male"),
        ('female',"Female"),

    ],
    max_length=100,null=True)

    gender=models.CharField(max_length=100,null=True)
    fullName=models.CharField(max_length=100,null=True)

    mobileNumber=models.IntegerField(null=True)
    age=models.IntegerField(null=True)
    dateOfBirth=models.DateField(null=True)
    presentAddress=models.CharField(max_length=100,null=True)
    permanentAddress=models.CharField(max_length=100,null=True)
    lastEducationName=models.CharField(max_length=100,null=True)
    instutiteName=models.CharField(max_length=100,null=True)
    passingYear=models.IntegerField(null=True)
    grade=models.IntegerField(null=True)
    profileimage=models.ImageField(upload_to='static/photo' ,null=True)