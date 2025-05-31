from django.db import models

# Create your models here.
class student(models.Model):
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    age= models.IntegerField()


class addTeacher(models.Model):
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    age= models.IntegerField()




class addCourse(models.Model):
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    courseCode = models.CharField(max_length=10, unique=True)
    credits = models.IntegerField(default=3)

