from django.db import models

# Create your models here.
class taskModel(models.Model):
    title=models.CharField(max_length=100, null=True)
    description=models.TextField(max_length=100, null=True)
    dueDate=models.DateField(null=True)
    priority=models.CharField(choices=[
        ('Low','Low'),
        ('Medium','Medium'),
        ('High','High'),
    ],max_length=100, null=True),
    status=models.CharField(choices=[
        ('Pending','Pending'),
        ('InProgress','InProgress'),
        ('Completed','Completed'),
    ],max_length=100,null=True)
    image=models.ImageField(upload_to="media/photo",null=True)
