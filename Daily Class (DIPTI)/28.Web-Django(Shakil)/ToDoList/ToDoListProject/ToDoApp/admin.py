from django.contrib import admin
from .models import *

# Register your models here.

class customUserDisplay(admin.ModelAdmin):
    
    list_display =['username','email','City']
    search_fields = ['username','email','City']
    
    fieldsets = [
        (
            "This is my title",
            {
                "fields":["username","email","password"]
            }
        ),
        (
            "Advanced Option",
            {
                "classes":["collapse"],
                "fields":["first_name","last_name","City","ProfilePic"]
            }
        ),
    ]

admin.site.register(CustomUserModel,customUserDisplay)
admin.site.register(CategoryModel)
admin.site.register(TaskModel)