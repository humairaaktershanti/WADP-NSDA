from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class eventUserModel(AbstractUser):
    fullName = models.CharField(max_length=100, null=True)
    phoneNumber = models.IntegerField(null=True)
    profileImage = models.ImageField(upload_to='static/dp', null=True)

class eventBookingModel(models.Model):
    EVENTTYPE = [
        ('Conference','Conference'),
        ('Concert','Concert'),
        ('Wedding','Wedding'),
    ]
    STATUS = [
        ('NotStart','Not Start'),
        ('InProgress','In Progress'),
        ('Completed','Completed'),
    ]
    eventTitle = models.CharField(max_length=100, null=True)
    eventType = models.CharField(max_length=100, choices=EVENTTYPE, null=True)
    eventDescription = models.TextField(null=True)
    eventDate = models.DateField(null=True)
    status = models.CharField(max_length=100, choices=STATUS, null=True)
    location = models.CharField(max_length=100, null=True)
    createdBy = models.ForeignKey(eventUserModel, on_delete=models.CASCADE, null=True)
    CreatedAt = models.DateTimeField(auto_now_add=True, null=True)
    updatedAt = models.DateTimeField(auto_now=True, null=True)