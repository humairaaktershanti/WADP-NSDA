from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return self.user.username
    
class oneModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    itemName = models.CharField(max_length=30, null=True, blank=True)
    COUNT = [
        ('One','One'),
        ('Two','Two'),
        ('Three','Three'),
    ]
    cunt = models.CharField(choices=COUNT, max_length=30, null=True, blank=True)
    totalItems = models.IntegerField(null=True, blank=True)
    addDate = models.DateField(auto_now_add=True)

class TwoModel(models.Model):
    companyName = models.CharField(max_length=30, null=True, blank=True)
    totalItems = models.IntegerField(null=True, blank=True)
    joiningDate = models.DateField(null=True, blank=True)
    addDate = models.DateField(auto_now_add=True)

class toDoModel(models.Model):
    title = models.CharField(max_length = 100, null = True)
    description = models.TextField(null = True)
    STATUS = [
        ('Not Started', 'Not Started'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]
    status = models.CharField(choices=STATUS, max_length=30, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add = True, null = True)
    updated_at = models.DateTimeField(auto_now = True, null = True)