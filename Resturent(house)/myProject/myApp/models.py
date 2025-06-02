from django.db import models

# Create your models here.
class ResturentModel(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    openingHours = models.CharField(max_length=100)


class FoodModel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    restaurant = models.ForeignKey(ResturentModel, on_delete=models.CASCADE, related_name='foods')

    