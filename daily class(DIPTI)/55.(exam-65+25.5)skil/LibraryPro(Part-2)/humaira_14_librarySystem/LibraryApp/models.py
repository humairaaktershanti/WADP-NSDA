from django.db import models
from django.contrib.auth.models import AbstractUser

class customUserModel(AbstractUser):
    USERTYPE = [
        ('Librarian','Librarian'),
        ('Student','Student'),
 
    ]
    userTypes = models.CharField(choices = USERTYPE, max_length = 100, null = True)

class librarianProfileModel(models.Model):
    user = models.ForeignKey(customUserModel, on_delete=models.CASCADE,null = True)
    employee_id = models.IntegerField(null = True)
    designation = models.TextField(null = True)
    contact_number = models.CharField(max_length=100,null = True)
    address = models.CharField(max_length=100,null = True)
    profile_picture = models.ImageField(upload_to = 'media/photo', null = True)

    def __str__(self):
        return self.employee_id
    
class studentProfileModel(models.Model):
    user = models.ForeignKey(customUserModel, on_delete=models.CASCADE,null = True)
    student_id = models.IntegerField(null = True)
    department = models.TextField(null = True)
    phone = models.CharField(max_length=100,null = True)
    address = models.CharField(max_length=100,null = True)
    profile_picture = models.ImageField(upload_to = 'media/photo', null = True)

    def __str__(self):
        return self.student_id
    
class bookModel(models.Model):
    librarianProfileModel = models.ForeignKey(librarianProfileModel, on_delete=models.CASCADE,null = True)
    title = models.TextField(null = True)
    author = models.TextField(null = True)
    isbn = models.IntegerField(null = True)
    quantity = models.IntegerField(null = True)
    created_at = models.DateField(auto_now_add=True, null = True)

    def __str__(self):
        return self.title