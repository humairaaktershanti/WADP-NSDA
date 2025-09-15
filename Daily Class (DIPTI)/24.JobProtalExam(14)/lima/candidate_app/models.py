from django.db import models
from users_auth_app.models import*
# Create your models here.


class CandidateProfileModel(models.Model):
    employer_user=models.OneToOneField(CustomUserModel , on_delete=models.CASCADE)
    full_name=models.CharField(max_length=100,null=True)
    phone=models.CharField(max_length=100,null=True)
    address=models.CharField(max_length=100,null=True)
    email=models.EmailField(null=True)
    date_of_birth=models.DateField(max_length=100,null=True)

