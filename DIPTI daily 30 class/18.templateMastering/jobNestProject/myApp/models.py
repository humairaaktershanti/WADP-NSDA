from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class customUserModel(AbstractUser):
    userType = models.CharField(max_length=20, choices=[
        ('jobSeekers', 'jobSeekers'), 
        ('recruiters', 'recruiters')],null=True,)
    
    def __str__(self):
        return self.username
    

# class jobPostModel(models.Model):
#     user=models.ForeignKey(customUser,on_delete=models.CASCADE,null=True)
#     jobTitle = models.CharField(max_length=100,null=True)
#     description = models.TextField(null=True)
#     salary = models.PositiveIntegerField(null=True)
#     location = models.CharField(max_length=100,null=True)
#     deadline = models.DateTimeField(null=True)

#     def __str__(self):
#         return self.jobTitle
    
# class applyJobModel(models.Model):
#     user=models.ForeignKey(customUser,on_delete=models.CASCADE,null=True)
#     jobPost=models.ForeignKey(jobPostModel,on_delete=models.CASCADE,null=True)
#     status=models.CharField(choices=[
#         ('Pending','Pending'),
#         ('Accept','Accept'),
#         ('Reject','Reject'),
#     ],max_length=100,null=True)