from django.db import models
from django.contrib.auth.models import AbstractUser

class AuthModel(AbstractUser):
    ...

class ProfileModel(models.Model):
    user = models.OneToOneField(AuthModel, on_delete=models.CASCADE, null=True)
    Name = models.CharField(max_length=100, null=True)
    Age = models.IntegerField(null=True)
    Height = models.IntegerField(null=True)
    Weight = models.IntegerField(null=True)
    GEN = [
        ('Male', 'Male'),
        ('Female', 'Female')
    ]
    Gender = models.CharField(max_length=100, choices=GEN, null=True)

class BMRModel(models.Model):
    BMR = models.IntegerField(null=True)
    Date = models.TimeField(auto_now_add=True ,null=True)

































# class ProfileModel(models.Model):
#     user = models.ForeignKey(AuthModel, on_delete=models.CASCADE, null=True)
#     Name = models.CharField(max_length=100, null=True)
#     Age = models.IntegerField(null=True)
#     Height = models.IntegerField(null=True)
#     Weight = models.IntegerField(null=True)
#     GEN = [
#         ('Male', 'Male'),
#         ('Female', 'Female')
#     ]
#     Gender = models.CharField(max_length=100, choices=GEN, null=True)

# class BMRModel(models.Model):
#     user = models.ForeignKey(ProfileModel, on_delete=models.CASCADE, null=True)
#     BMR = models.IntegerField(null=True)
#     Date = models.TimeField(auto_now_add=True ,null=True)