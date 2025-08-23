from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

# -------------------------
# User & Profile
# -------------------------
class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('employee', 'Employee'),
        ('student', 'Student'),
    ]
    SUBROLE_CHOICES = [
        ('faculty', 'Faculty'),
        ('hr', 'HR'),
        ('finance', 'Finance'),
        ('marketing', 'Marketing'),
        ('it', 'IT'),
        ('teacher', 'Teacher'),
        ('other', 'Other'),
        ('regular_student', 'Regular Student'),
        ('online_student', 'Online Student'),
        ('diploma_student', 'Diploma Student'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    sub_role = models.CharField(max_length=30, choices=SUBROLE_CHOICES, blank=True, null=True)
    # Profile fields
    image = models.ImageField(upload_to="profiles/", blank=True, null=True)
    bio = models.TextField(blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True)
    gender = models.CharField(max_length=10, blank=True)
    location = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=50, blank=True)
    # Social links
    facebook = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    
    def __str__(self):
        return f"{self.username} ({self.role})"

# -------------------------
# Notifications & Logs
# -------------------------
class Notification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField()
    action_link = models.URLField(blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class AuditLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=255)
    model_name = models.CharField(max_length=100)
    object_id = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

# -------------------------
# Trash (Soft Delete Backup)
# -------------------------
class Trash(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    model_name = models.CharField(max_length=100)
    object_data = models.JSONField()   # Store deleted object as JSON
    deleted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    deleted_at = models.DateTimeField(auto_now_add=True)