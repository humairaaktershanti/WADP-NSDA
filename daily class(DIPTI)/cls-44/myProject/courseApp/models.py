from django.db import models
from authApp.models import *

class courseModel(models.Model):
    assignTeacher=models.ForeignKey(teacherModel,on_delete=models.CASCADE,null=True)
    courseTitle=models.CharField(max_length=100,null=True)
    courseDescription=models.TextField(null=True)
    courseDuration=models.IntegerField(null=True)
    courseStartDate=models.DateField(null=True)
    courseFee=models.IntegerField(null=True)

class admittedModel(models.Model):
    student=models.ForeignKey(studentModel,on_delete=models.CASCADE,null=True)
    admittedCourse=models.ForeignKey(courseModel,on_delete=models.CASCADE,null=True)
    payment=models.IntegerField(null=True)
    due=models.IntegerField(null=True)
    admittedDate=models.DateField(auto_now_add=True,null=True)