from django.db import models

# Create your models here.
from django.db import models
class courseModel(models.Model):
    name=models.CharField(max_length=100,null=True)
    duration=models.DateField(auto_now=True,null=True)
    description=models.TextField(null=True)
 