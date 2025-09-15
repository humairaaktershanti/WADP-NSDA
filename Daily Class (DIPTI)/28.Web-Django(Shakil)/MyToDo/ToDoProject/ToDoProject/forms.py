from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django import forms
from ToDoApp.models import *

class CustomToDoUserForm(UserCreationForm):
    class Meta:
        model = CustomToDoUserModel
        fields = UserCreationForm.Meta.fields+("first_name","last_name","email","email","ProfilePic","UserType")

class CustomToDoUserAuthentationForm(AuthenticationForm):
    class Meta:
        model = CustomToDoUserModel
        fields = ("username","password")
    
class CategoryForm(forms.ModelForm):
    class Meta:
        model = CategoryModel
        fields = ['CategoryName']