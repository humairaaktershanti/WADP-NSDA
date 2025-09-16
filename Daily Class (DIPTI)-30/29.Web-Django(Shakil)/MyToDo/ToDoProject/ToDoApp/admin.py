from django.contrib import admin
from ToDoApp.models import *

# Register your models here.
class CustomUserDisplay(admin.ModelAdmin):
    list_display = ['username','first_name','email']
    search_fields = ['username','email']
    
    fieldsets = [
        (
            "User Information",
        {
            "fields":["username","first_name","last_name","email","password"]
        }
        )
    ]

admin.site.register(CustomToDoUserModel,CustomUserDisplay)

class categoryDisplay(admin.ModelAdmin):
    list_display = ['CategoryName','user']
admin.site.register(CategoryModel,categoryDisplay)
admin.site.register(TaskModel)