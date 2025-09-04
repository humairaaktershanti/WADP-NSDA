from django.db import models

# Create your models here.
class storeModel(models.Model):
    StoreName=models.CharField(max_length=30)
    OwnerName=models.CharField(max_length=50)
    StoreLocation=models.CharField(max_length=30)
    
