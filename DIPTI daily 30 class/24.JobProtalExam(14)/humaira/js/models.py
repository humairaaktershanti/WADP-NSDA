from django.db import models
from django.contrib.auth.models import AbstractUser

class customUserModel(AbstractUser):
    USERTYPE = [
        ('Admin','Admin'),
        ('Student','Student'),
        ('Teacher','Teacher')
    ]
    userTypes = models.CharField(choices = USERTYPE, max_length = 100, null = True)
    fullName = models.CharField(max_length = 100, null = True)
    dateOfBirth = models.DateField(null = True)
    profileImage = models.ImageField(upload_to = "static/img/DP", null = True)

class studentModel(models.Model):
    studentName = models.CharField(max_length = 100,null = True)
    studentBio = models.TextField(null = True)
    studentAge = models.IntegerField(null = True)
    studentImage = models.ImageField(upload_to = 'static/img/student')
    createdAt = models.DateTimeField(auto_now_add = True, null = True)
    updateAt = models.DateTimeField(auto_now = True, null = True)