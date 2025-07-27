from django.db import models

# Create your models here.
class studentModel(models.Model):
    studentName=models.CharField(max_length=100,null=True)
    addressName=models.CharField(max_length=100,null=True)
    age=models.IntegerField(null=True)
    registerDate=models.DateField(null=True)

    def __str__(self):
        return self.studentName
    

    