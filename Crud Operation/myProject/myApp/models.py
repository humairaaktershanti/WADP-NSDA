from django.db import models

# Create your models here.
class studentModel(models.Model):
    name=models.CharField(max_length=100)
    age=models.IntegerField()
    address=models.TextField()
    image=models.ImageField(upload_to="media/upload")