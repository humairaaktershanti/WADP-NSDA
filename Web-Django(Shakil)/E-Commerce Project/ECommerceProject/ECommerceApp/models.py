from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class ECommerceUser(AbstractUser):
    FullName = models.CharField(max_length=100)
    USERTYPE = {
        ('Customer','Customer'),
        ('Seller','Seller'),
    }
    
    UserType = models.CharField(choices=USERTYPE,max_length=100)
    GENDER = {
        ('Male','Male'),
        ('Female','Female'),
    }
    
    Gender = models.CharField(choices=GENDER,max_length=100)
    ProfileImg = models.ImageField(upload_to='static/img/')
    
class CustomerInfoModel(models.Model):
    EUser = models.OneToOneField(ECommerceUser,on_delete= models.CASCADE, related_name = 'customerinfomodel')
    InterestedProduct = models.CharField(max_length=100)
    ReferenceID = models.CharField(max_length=100)
    
    def __str__(self):
        return self.EUser.FullName+"-"+self.EUser.UserType+"-"+self.ReferenceID
    
class SellerInfoModel(models.Model):
    EUser = models.OneToOneField(ECommerceUser,on_delete= models.CASCADE, related_name = 'sellerinfomodel')
    CompanyName = models.CharField(max_length=100)
    CompanyAddress = models.CharField(max_length=100)
    SellingExperience = models.CharField(max_length=100)
    
    def __str__(self):
        return self.EUser.FullName+"-"+self.EUser.UserType+"-"+self.CompanyName
    
class ContactInfoModel(models.Model):
    EUser = models.OneToOneField(ECommerceUser,on_delete= models.CASCADE, related_name = 'contactinfomodel')
    Mobile = models.CharField(max_length=100)    
    Address = models.CharField(max_length=100)    
    FacebookID = models.CharField(max_length=100)  
    
    def __str__(self):
        return self.EUser.FullName+"-"+self.EUser.UserType+"-"+self.Mobile  
    
class ProductModel(models.Model):
    ProductName = models.CharField(max_length=100)
    PRODUCTCATEGORY = {
        ('Electric','Electric'),
        ('Beauty','Beauty'),
        ('Food','Food'),
    }
    ProductCategory = models.CharField(choices=PRODUCTCATEGORY,max_length=100)
    ProductDescription = models.TextField()   
    ProCompanyName = models.CharField(max_length=100) 
    ProCompanyAddress = models.CharField(max_length=100) 
    ProductPrice = models.CharField(max_length=100) 
    Added_by = models.ForeignKey(ECommerceUser,on_delete=models.CASCADE)
    