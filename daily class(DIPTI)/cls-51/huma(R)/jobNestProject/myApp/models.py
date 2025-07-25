from django.db import models
from django.contrib.auth.models import AbstractUser

# for custom user
class customUserModel(AbstractUser):
    userType = models.CharField(max_length=20, choices=[
        ('jobSeekers', 'jobSeekers'), 
        ('recruiters', 'recruiters')],null=True,)
    def __str__(self):
        return self.username
    
# for recruiters
class recruitersModel(models.Model):
    employerUser = models.OneToOneField(customUserModel, on_delete = models.CASCADE, null = True)
    companyName = models.CharField(max_length = 100, null = True)
    aboutConpany = models.TextField(null = True)
    conpanyLogo = models.ImageField(upload_to='static/img/logo', null = True)
    location = models.TextField(null = True)
    def __str__(self):
        return self.companyName

class jobModel(models.Model):
    employer = models.ForeignKey(recruitersModel, on_delete = models.CASCADE, null = True)
    title = models.CharField(max_length = 100, null = True)
    description = models.TextField(null = True)
    requirements = models.TextField(null = True)
    salary = models.IntegerField(null = True)
    TYPE = [
        ('FullTime','Full Time'),
        ('Remote','Remote'),
        ('Internship','Internship')
    ]
    jobType = models.CharField(choices = TYPE, max_length = 100, null = True)
    deadline = models.DateField(null = True)
    postedDate = models.DateTimeField(auto_now_add = True, null = True)
    def __str__(self):
        return self.title

# for jobSeekers
class jobSeekersModel(models.Model):
    candidateUser = models.OneToOneField(customUserModel, on_delete = models.CASCADE, null = True)
    fullName = models.CharField(max_length = 100, null = True)
    adress = models.TextField(null = True)
    dateOfBirth = models.DateField(null = True)
    def __str__(self):
        return self.fullName

class jobApplicationModel(models.Model):
    job = models.ForeignKey(jobModel, on_delete = models.CASCADE, null = True)
    candidate = models.ForeignKey(jobSeekersModel, on_delete = models.CASCADE, null = True)
    STATUS = [
        ('Applied','Applied'),
        ('Interview','Interview'),
        ('Offered','Offered'),
        ('Rejected','Rejected')
    ]
    status = models.CharField(choices = STATUS, max_length = 100, null = True)
    appliedAt = models.DateTimeField(auto_now_add = True, null = True)
    def __str__(self):
        return self.status