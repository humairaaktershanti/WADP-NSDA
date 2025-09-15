from django.db import models

# Create your models here.
class taskModel(models.Model):
    
    title=models.CharField(max_length=100,null=True)
    description=models.TextField(null=True)
    dueDate=models.DateField(null=True)
    priority=models.CharField(choices=[
            ('low','Low'),
            ('medium','Medium'),
            ('high','High'),
        ],max_length=10, null=True)
    status=models.CharField(choices=[
            ('pending','Pending'),
            ('inprogress','Inprogress'),
            ('completed','Completed'),
        ],max_length=10, null=True)




    