from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils.text import slugify
from ckeditor.fields import RichTextField

class CustomUserModel(AbstractUser):
    USER_ROLES = [
        ('Admin', 'Admin'),
        ('Author', 'Author'),
    ]

    role = models.CharField(max_length=20, choices=USER_ROLES, default='Author', null=True)
    phone = models.CharField(max_length=15, null=True)
    profile = models.ImageField(upload_to="profile/", null=True, blank=True)
    
    def __str__(self):
        return self.first_name
    



class CategoryModel(models.Model):
    catagory_name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.catagory_name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.catagory_name)  
        super().save(*args, **kwargs)
    
    
    
class NewsModel(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Published', 'Published'),
        ('Rejected', 'Rejected'),
    ]

    title = models.CharField(max_length=255)
    content = RichTextField(null=True)
    excerpt = models.TextField(blank=True, null=True, help_text="Short summary of the news")
    category = models.ForeignKey(CategoryModel, on_delete=models.SET_NULL, null=True, related_name='news')
    author = models.ForeignKey(CustomUserModel, on_delete=models.SET_NULL, null=True, related_name='news_articles')
    featured_image = models.ImageField(upload_to='news_images/', null=True, blank=True)
    published_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views_count = models.PositiveIntegerField(default=0)