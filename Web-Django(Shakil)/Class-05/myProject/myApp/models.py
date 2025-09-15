from django.db import models

# Create your models here.
class studentModel(models.Model):
    
    name= models.CharField(max_length=100)
    roll= models.CharField(max_length=100)
    department= models.CharField(max_length=100)
    city= models.CharField(max_length=100)
    
    def __str__(self):
        return self.name +"-"+ self.department

class classModel(models.Model):
    
    classname= models.CharField(max_length=100)
    classid= models.CharField(max_length=100)
    totalstudent= models.CharField(max_length=100)
    
    def __str__(self):
        return self.classname +"-"+ self.classid

class studentfamily(models.Model):
    studentaddress= models.CharField(max_length=100)
    studentid= models.CharField(max_length=100)
    studentfather= models.CharField(max_length=100)
    
    def __str__(self):
        return self.studentfather +"-"+ self.studentaddress
    

class studentfriends(models.Model):
    friendsname= models.CharField(max_length=100)
    friendid= models.CharField(max_length=100)
    friendaddress= models.CharField(max_length=100)
    
    def __str__(self):
        return self.friendsname +"-"+ self.friendid
    
class studentskill(models.Model):
    skillname= models.CharField(max_length=100)
    skillid= models.CharField(max_length=100)
    
    def __str__(self):
        return self.skillname +"-"+ self.skillid

class studenthobby(models.Model):
    hobbyname= models.CharField(max_length=100)
    hobbyid= models.CharField(max_length=100)
    
    def __str__(self):
        return self.hobbyname +"-"+ self.hobbyid