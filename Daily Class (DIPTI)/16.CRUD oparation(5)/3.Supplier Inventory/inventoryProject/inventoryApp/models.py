from django.db import models
class supplierModel(models.Model):
    name=models.CharField(max_length=100,null=True)
    email=models.EmailField(null=True)
    phone=models.CharField(max_length=100,null=True)
 

# Create your models here.
