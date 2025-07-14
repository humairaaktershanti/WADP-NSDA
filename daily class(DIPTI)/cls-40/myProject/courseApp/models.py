from django.db import models
from authApp.models import *

class courseModel(models.Model):
    assignTeacher=models.ForeignKey(teacherModel,on_delete=models.CASCADE,null=True)
    courseTitle=models.CharField(max_length=100,null=True)
    courseDescription=models.TextField(null=True)
    courseDuration=models.PositiveIntegerField(null=True)
    courseStartDate=models.DateField(null=True)
    courseFee=models.PositiveIntegerField(null=True)

class admittedModel(models.Model):
    student=models.ForeignKey(studentModel,on_delete=models.CASCADE,null=True)
    admittedCourse=models.ForeignKey(courseModel,on_delete=models.CASCADE,null=True)
    payment=models.PositiveIntegerField(null=True)
    due=models.PositiveIntegerField(null=True)
    admittedDate=models.DateField(auto_now_add=True,null=True)