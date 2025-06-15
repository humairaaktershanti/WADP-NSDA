from django.db import models

# Create your models here.
class UserAuthModel(models.Model):
    username=models.CharField(max_length=50)
    full_name=models.CharField(max_length=100)
    email=models.EmailField()
    contact_number=models.CharField(max_length=15)
    password=models.CharField(max_length=10)
    creat_at=models.DateTimeField(auto_now_add=True)