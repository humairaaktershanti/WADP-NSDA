from django.db import models
from django.contrib.auth.models import AbstractUser

#customuserModel 
class customuserModel(AbstractUser):
    profile_photo=models.ImageField(upload_to='media/image')
    bio=models.TextField()
    
#task model
class taskModel(models.Model):
    PRIORITY_TYPE=[
        ('Low','Low'),
        ('Medium','Medium'),
        ('High','High'),
    ]
    user=models.ForeignKey(customuserModel, on_delete=models.CASCADE, null=True)
    
    title=models.CharField(max_length=100, null=True)
    description=models.TextField()
    due_date=models.DateField(null=True)
    priority=models.CharField(choices=PRIORITY_TYPE, max_length=20, null=True)
    status=models.CharField(choices=[
        ('Pending','Pending'),
        ('In progress','In progress'),
        ('Completed','Completed'),
    ],
        max_length=20, null=True)
    
    created_at=models.DateTimeField(auto_now_add=True, null=True)
    