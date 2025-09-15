from django.db import models
from django.conf import settings

class EmployerProfileModel(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='employer_profile'
    )

    company_name = models.CharField(max_length=100)
    emaile = models.EmailField(null=True)
    phone = models.CharField(max_length=100, null=True)
    about_company = models.TextField(null=True)
    company_logo = models.ImageField(upload_to='Media/photo', null=True)
    location = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.company_name

    