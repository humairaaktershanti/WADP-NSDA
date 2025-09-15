from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class customUserModel(AbstractUser):
    userTypes = models.CharField(choices=[
        ('Admin', 'Admin'),
        ('Employee', 'Employee'),
    ],null=True,max_length=100)

class departmentModel(models.Model):
    name=models.CharField(max_length=100,null=True)
    describtion=models.TextField(null=True)

class employeeModel(models.Model):
    user=models.OneToOneField(customUserModel,on_delete=models.CASCADE, null=True)
    department=models.ForeignKey(departmentModel, on_delete=models.CASCADE, null=True)    
    fullName=models.CharField(max_length=100,null=True)
    phone=models.CharField(max_length=100,null=True)
    position=models.CharField(max_length=100,null=True)
    dateOfJoining=models.DateField(null=True)
    profilePicture=models.ImageField(upload_to='media/photo', null=True)
class leaveModel(models.Model):
    employee = models.ForeignKey(employeeModel, on_delete=models.CASCADE, null=True)
    leaveType = models.CharField(choices=[
        ('SickLeave', 'SickLeave'),
        ('CasualLeave', 'CasualLeave'),
        ('EarnedLeave', 'EarnedLeave'),
    ], max_length=100, null=True)

    fromDate = models.DateField(null=True)
    toDate = models.DateField(null=True)

    status = models.CharField(choices=[
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ], max_length=100, null=True)


# class approveRejectModel(models.Model):
#     adminUser = models.OneToOneField(customUserModel,on_delete=models.CASCADE, null=True)
#     leave = models.ForeignKey(leaveModel,on_delete=models.CASCADE, null=True)
#     AppRej = models.CharField(choices=[
#         ('Approved', 'Approved'),
#         ('Rejected', 'Rejected'),
#     ], max_length=100, null=True)

#     def __str__(self):
#         return self.AppRej