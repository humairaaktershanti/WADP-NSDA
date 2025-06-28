from django.db import models

# Create your models here.
class To_DoModel(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=20)
    due_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    
   