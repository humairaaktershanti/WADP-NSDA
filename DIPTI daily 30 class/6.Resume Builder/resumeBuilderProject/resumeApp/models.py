from django.db import models

# Create your models here.
class ResumeModel(models.Model):
    fullName=models.CharField(max_length=100)
    profilePicture=models.ImageField(upload_to="media/photo")
    email=models.EmailField()
    phone=models.CharField(max_length=50)
    address=models.TextField()
    summary=models.TextField()
    degree=models.CharField(max_length=50)
    instituteName=models.CharField(max_length=50)
    yearsOfGraduation=models.IntegerField()
    companyName=models.CharField(max_length=50)
    position=models.CharField(max_length=50)
    yearsOfExperience=models.IntegerField()
    skills=models.TextField()
    hobbies=models.TextField()
    achievements=models.TextField()
