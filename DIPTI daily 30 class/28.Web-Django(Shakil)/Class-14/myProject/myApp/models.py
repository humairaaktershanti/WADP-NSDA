from django.db import models

# Create your models here.
class studentModel(models.Model):
    FirstName=models.CharField(max_length=30)
    LastName=models.CharField(max_length=30)
    Department=models.CharField(max_length=30)
    StudentImage=models.ImageField(upload_to='media/images/',null=True)