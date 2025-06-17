from django.db import models

# Create your models here.
class RestaurantModel(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    phoneNumber = models.CharField(max_length=15)
    email = models.EmailField()
    cuisineType = models.CharField(max_length=50)