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

class AddCash(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    source = models.CharField(max_length=100, null=True)
    datetime = models.TimeField(auto_now_add=True, null=True)
    amount = models.IntegerField(null=True)
    description = models.TextField(null=True)

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    description = models.TextField(null=True)
    amount = models.IntegerField(null=True)
    datetime = models.TimeField(auto_now_add=True, null=True)

class CashManagement(models.Model):
    expense = models.ForeignKey(User, on_delete=models.CASCADE, null=True)