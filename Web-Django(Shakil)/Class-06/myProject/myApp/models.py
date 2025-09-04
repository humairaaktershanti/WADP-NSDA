from django.db import models

# Create your models here.
class studentModel(models.Model):
    name= models.CharField(max_length=100)
    rollno = models.CharField(max_length=30)
    dept = models.CharField(max_length=30)
    
    def __str__(self):
        return self.rollno+"-"+ self.name

class teacherModel(models.Model):
    teachername = models.CharField(max_length=50)
    teacherid = models.CharField(max_length=20)
    designation =models.CharField(max_length=50)
    
    def __str__(self):
        return self.teacherid+"-"+self.teachername

class managementModel(models.Model):
    name = models.CharField(max_length=50)
    managementid = models.CharField(max_length=20)
    address =models.CharField(max_length=50)
    
    def __str__(self):
        return self.managementid+"-"+self.name

class staffModel(models.Model):
    staffname = models.CharField(max_length=50)
    staffage = models.CharField(max_length=20)
    address =models.CharField(max_length=50)
    
    def __str__(self):
        return self.staffname+"-"+self.address

class libraryModel(models.Model):
    libraryid = models.CharField(max_length=50)
    librarytype = models.CharField(max_length=20)
    
    def __str__(self):
        return self.libraryid+"-"+self.librarytype
    
    
