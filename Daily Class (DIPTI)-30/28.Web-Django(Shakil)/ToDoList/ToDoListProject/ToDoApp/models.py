from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUserModel(AbstractUser):
    USERTYPE = [
        ('Admin','Admin'),
        ('Viewer','Viewer'),
    ]
    UserType = models.CharField(choices=USERTYPE,max_length=100, null=True)
    City = models.CharField(max_length=100, null=True)
    ProfilePic = models.ImageField(upload_to='media/profilePic/',null=True)
    
    class Meta:
        ordering = ["username"]
        verbose_name = "Custom User"
        db_table = "To_Do_List_Table"
        unique_together = ["username","email"]
        
class CategoryModel(models.Model):
    user = models.ForeignKey(CustomUserModel,on_delete =models.CASCADE, null = True)
    CategoryName = models.CharField(max_length=100,null=True)
    Create_date = models.DateField(null=True)
    Update_date = models.DateField(auto_now=True,null=True)
    
class TaskModel(models.Model):
    PRIORITY = [
        ("High","High"),
        ("Medium","Medium"),
        ("Low","Low"),
    ]
    category = models.ForeignKey(CategoryModel,on_delete=models.CASCADE,null=True)
    Priority = models.CharField(choices=PRIORITY,max_length=100,null=True)
    TaskName = models.CharField(max_length=100,null=True)
    TaskDescription = models.TextField(null=True)
    Status = models.CharField(max_length=100, default="On_Going",null=True)
    Create_date = models.DateField(null=True)
    Update_date = models.DateField(auto_now=True,null=True)
    Due_date = models.DateField(auto_now_add=True,null=True)
    Complete_date = models.DateField(null=True)
    
    class Meta:
        
        ordering = ["category"]
        verbose_name = "Task Data Model"
        db_table = "Task_Data_Table"
        
    