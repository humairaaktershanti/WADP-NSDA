from django.db import models

# Create your models here.
class bookModel(models.Model):
    title=models.CharField(max_length=100,null=True)
    author=models.CharField(max_length=100,null=True)
    isbn=models.CharField(max_length=100,null=True)
    coverImage=models.ImageField(upload_to='media/photo',null=True)
    publishedDate=models.DateField(auto_now=True,null=True)