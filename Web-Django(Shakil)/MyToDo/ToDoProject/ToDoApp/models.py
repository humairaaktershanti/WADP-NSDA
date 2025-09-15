from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomToDoUserModel(AbstractUser):
    USERTYPE = [
        ('Admin','Admin'),
        ('Viewer','Viewer'),
    ]
    UserType = models.CharField(choices=USERTYPE,max_length=100,null=True)
    ProfilePic = models.ImageField(upload_to='media/profilepic/',null=True)

    class Meta:
        ordering = ["username"]
        verbose_name = "Custom User"
        db_table = "to_do_user_table"
        unique_together = ["username","email"]

class CategoryModel(models.Model):
    user = models.ForeignKey(CustomToDoUserModel,on_delete=models.CASCADE,null=True)
    CategoryName = models.CharField(max_length=100,null=True)
    Created_at = models.DateField(auto_now_add=True,null=True)
    Updated_at = models.DateField(auto_now=True,null=True)
    
    class Meta:
        ordering=['CategoryName']
        verbose_name = "Category Info"
        db_table = "category_name_table"

class TaskModel(models.Model):
    PRIORITY = [
        ("High","High"),
        ("Medium","Medium"),
        ("Low","Low"),
    ]
    category = models.ForeignKey(CategoryModel,on_delete=models.CASCADE,null=True)
    Priority = models.CharField(choices=PRIORITY,max_length=100, null=True)
    TaskName = models.CharField(max_length=100,null=True)    
    TaskDescription = models.CharField(max_length=100,null=True)    
    Status = models.CharField(max_length=100,null=True)    
    Created_at = models.DateField(auto_now_add=True,max_length=100,null=True)    
    Updated_at = models.DateField(auto_now=True,max_length=100,null=True)    
    DueDate = models.DateField(max_length=100,null=True)    
    
    class Meta:
        ordering = ["category"]
        verbose_name = "Task Data Model"
        db_table = "task_data_table"