from django.db import models

# Create your models here.
class book(models.Model):
    title=models.CharField(max_length=100)
    author=models.CharField(max_length=100)
    price=models.IntegerField()
    stock=models.CharField()
    published_date=models.DateField()


class user(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    address=models.CharField()
    phone=models.IntegerField() 