from django.db import models

# Create your models here.
class studentModel(models.Model):
    name=models.CharField(max_length=100)
    roll_no=models.IntegerField(max_length=100)
    department=models.CharField(max_length=100)
    student_image=models.ImageField(upload_to="Media/Photo")
    created_at=models.DateTimeField(auto_now=True)


class toDoModel(models.Model):
    title=models.CharField(max_length=100)
    description=models.TextField()
    status=models.CharField(max_length=100)
    due_date=models.DateField()
    created_at=models.DateTimeField(auto_now=True)    