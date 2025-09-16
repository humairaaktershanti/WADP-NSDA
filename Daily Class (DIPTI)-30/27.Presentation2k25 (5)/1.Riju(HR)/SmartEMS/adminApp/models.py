from django.db import models
from customUserAuth.models import CustomUserAuthModel
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.
class DepartmentModel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class DesignationModel(models.Model):
    title = models.CharField(max_length=100)
    department = models.ForeignKey(DepartmentModel, on_delete=models.CASCADE, related_name='department_info')
    
    def __str__(self):
        return self.title
    
class ProfileModel(models.Model):
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )
    user = models.OneToOneField(CustomUserAuthModel, on_delete=models.CASCADE, related_name='profile')
    employee_id = models.CharField(max_length=20, unique=True)
    full_name= models.CharField(max_length=150, null=True)
    position = models.ForeignKey(DesignationModel, on_delete=models.SET_NULL, null=True, blank=True, related_name='designation_info')
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    birthday = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)
    date_of_joining = models.DateField(null=True, blank=True)
    profile_image = models.ImageField(upload_to='profiles/', null=True, blank=True)
    reports_to = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subordinates')
    
    def __str__(self):
        return f"{self.full_name}'s Profile"
    @property
    def is_team_lead(self):
        return self.teams.filter(role='Lead').exists()
    

class HolidayModel(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['date']
    
    def __str__(self):
        return self.title
    
    @property
    def is_past(self):
        return self.date < timezone.now().date()
    
    @property
    def day_name(self):
        return self.date.strftime('%A')
    
class NoticeModel(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(CustomUserAuthModel, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    

class PromotionModel(models.Model):
    employee = models.ForeignKey(ProfileModel, on_delete=models.CASCADE, related_name='promotions')
    department = models.ForeignKey(DepartmentModel, on_delete=models.SET_NULL, null=True, blank=True)
    designation_from = models.ForeignKey(DesignationModel, on_delete=models.SET_NULL, null=True, blank=True, related_name='designation_from')
    designation_to = models.ForeignKey(DesignationModel, on_delete=models.SET_NULL, null=True, blank=True, related_name='designation_to')
    promotion_date = models.DateField()

    class Meta:
        ordering = ['-promotion_date']

    def __str__(self):
        return f"{self.employee.full_name} promoted to {self.designation_to.name}"
    
class ResignationModel(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    employee = models.ForeignKey(ProfileModel, on_delete=models.CASCADE, related_name='resignations')
    department = models.ForeignKey(DepartmentModel, on_delete=models.SET_NULL, null=True, blank=True)
    reason = models.TextField()
    notice_date = models.DateField()
    resignation_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    actioned_by = models.ForeignKey(ProfileModel, null=True, blank=True, on_delete=models.SET_NULL, related_name='resignation_actioned')
    actioned_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Resignation"
        verbose_name_plural = "Resignations"
        ordering = ['-resignation_date']

    def __str__(self):
        return f"{self.employee.full_name} - {self.resignation_date}"

class ActivityLogModel(models.Model):
    user = models.ForeignKey(CustomUserAuthModel, on_delete=models.CASCADE)
    action = models.CharField(max_length=50)
    object_repr = models.CharField(max_length=255)
    object_id = models.PositiveIntegerField(null=True, blank=True) 
    model_name = models.CharField(max_length=50, blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)



class TerminationModel(models.Model):
    TERMINATION_TYPE_CHOICES = [
    ('Misconduct', 'Misconduct'),
    ('Performance', 'Performance'),
    ('Other', 'Other'),
    ]
    employee = models.ForeignKey(ProfileModel, on_delete=models.CASCADE)
    department = models.ForeignKey(DepartmentModel, on_delete=models.SET_NULL, null=True, blank=True)
    termination_type = models.CharField(max_length=50, choices=TERMINATION_TYPE_CHOICES)
    termination_date = models.DateField()
    notice_date = models.DateField()
    reason = models.TextField()

    def __str__(self):
        return f"{self.employee.full_name} - {self.termination_type}"
    

class Role(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class User(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name
    