from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Recipe_User(AbstractUser):
    USER=[
        ('Chef','Chef'),
        ('Viewers','Viewers')
    ]
    
    GENDER=[
        ('Male','Male'),
        ('Female','Female')
    ]
    
    Gender = models.CharField(choices=GENDER,max_length=100,null=True)
    UserType= models.CharField(choices=USER,max_length=100,null=True)
    City=models.CharField(max_length=100,null=True)
    Age=models.CharField(max_length=100,null=True)
    Country=models.CharField(max_length=100,null=True)

class addRecipeModel(models.Model):
    DIFLEVEL=[
        ('High','High'),
        ('Medium','Medium'),
        ('Low','Low'),
    ]
    TAGS=[
        ('Vegetrian','Vegetrian'),
        ('Non-Vegetrian','Non-Vegetrian'),
    ]
    RECIPECATE=[
        ('Breakfast','Breakfast'),
        ('Lunch','Lunch'),
        ('Dinner','Dinner'),
    ]
    RecipeTitle= models.CharField(max_length=100,null=True)
    Ingredients= models.TextField(null=True)
    Instructions= models.TextField(null=True)
    
    PreparationTime= models.CharField(max_length=100,null=True)
    CookingTime= models.CharField(max_length=100,null=True)
    TotalTime= models.CharField(max_length=100,null=True)
    NutritionalInformation=models.CharField(max_length=100,null=True)
    TotalCalorie=models.CharField(max_length=100,null=True)
    
    Tags= models.CharField(choices=TAGS,max_length=100,null=True)
    RecipeCategory= models.CharField(choices=RECIPECATE,max_length=100,null=True)
    DifficultyLevel= models.CharField(choices=DIFLEVEL,max_length=100,null=True)
    SampleImage=models.ImageField(upload_to='static/img/',null=True)
    Create_by = models.ForeignKey(Recipe_User,on_delete=models.CASCADE,null=True)
