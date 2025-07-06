from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class productModel(models.Model):
    productName=models.CharField(max_length=100,null=True)
    productDescription=models.TextField(null=True)
    productPrice=models.IntegerField(null=True)
    productImage=models.ImageField(upload_to='Static/Photo')
    created_at=models.DateTimeField(auto_now_add=True,null=True)



class customerUser(AbstractUser):
    user_types=models.CharField(choices=[
        ('customer','Customer'),
        ('owner','Owner'),
        
    ],
    max_length=100,null=True)

    fullName=models.CharField(max_length=100,null=True)
    email=models.EmailField(null=True)
    dateOfBirth=models.DateField(null=True)
    profileImage=models.ImageField(upload_to="media/photo",null=True)








    
