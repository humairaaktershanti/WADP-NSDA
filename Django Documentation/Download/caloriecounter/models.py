from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    height = models.FloatField(help_text="Height in cm")
    weight = models.FloatField(help_text="Weight in kg")
    bmr = models.FloatField(blank=True, null=True, help_text="Basal Metabolic Rate")
    daily_calorie_goal = models.FloatField(blank=True, null=True, help_text="Daily calorie goal")
    
    def calculate_bmr(self):
        if self.gender == 'male':
            self.bmr = 66.47 + (13.75 * self.weight) + (5.003 * self.height) - (6.755 * self.age)
        else:
            self.bmr = 655.1 + (9.563 * self.weight) + (1.850 * self.height) - (4.676 * self.age)
        self.save()
        return self.bmr
    
    def __str__(self):
        return self.user.username

class ConsumedCalorie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100)
    calories = models.FloatField()
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.item_name} - {self.calories} cal"
    
    class Meta:
        ordering = ['-date', '-time']