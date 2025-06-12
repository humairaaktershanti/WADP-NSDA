from django.db import models

# Create your models here.
class ToDoModel(models.Model):
    title=models.CharField(max_length=100)
    description=models.TextField(max_length=100)
    status=models.CharField(max_length=100,choices=[
            ('pending', 'Panding'),
            ('in_prograss', 'In Progress'),
            ('completed', 'Completed')
        ],
    default='pending'
    )
    due_date=models.DateField()
    created_at=models.DateField(auto_now_add=True)
