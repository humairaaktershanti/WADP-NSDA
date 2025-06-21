from django.db import models

# Create your models here.
class profileModel(models.Model):
    name=models.CharField(max_length=100)
    date_of_birth=models.DateField()
    profile_photo=models.ImageField()