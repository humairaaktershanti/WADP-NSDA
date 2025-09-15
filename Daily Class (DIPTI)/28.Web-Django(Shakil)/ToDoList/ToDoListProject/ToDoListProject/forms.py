from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from ToDoApp.models import *

class myUserCreationForm(UserCreationForm):
    class Meta:
        model= CustomUserModel
        fields = UserCreationForm.Meta.fields+("first_name","last_name","email","City","ProfilePic","UserType")
        
class myAuthenticationForm(AuthenticationForm):
    class Meta:
        model= CustomUserModel
        fields = ("username","password")
        