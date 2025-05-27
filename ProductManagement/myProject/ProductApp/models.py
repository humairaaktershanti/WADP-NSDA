from django.db import models

# Create your models here.
class productModel(models.Model):

    name= models.CharField(max_length=100)
    email=models.EmailField()
    contact=models.CharField(max_length=100)
    address=models.TextField(max_length=100)

class customerModel(models.Model):

    name= models.CharField(max_length=100)
    email=models.EmailField()
    contact=models.CharField(max_length=100)
    address=models.TextField(max_length=100)    