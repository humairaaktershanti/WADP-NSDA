from django.db import models

# Create your models here.
class book(models.Model):
    Title=models.CharField(max_length=100, null=True)
    Author=models.CharField(max_length=100, null=True)
    BookCategory=models.CharField(max_length=100, null=True)
    PublishDate=models.DateField(auto_now_add=True, null=True)
    Description=models.TextField(max_length=100, null=True)
    Cover_Photo=models.ImageField(upload_to="Media/Cover_Photo", null=True)