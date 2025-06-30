from django.contrib import admin
from myApp.models import *

# Register your models here.
from django.contrib.auth.admin import UserAdmin


class userModel(UserAdmin):
    list_display=['username','email','user_type']

admin.site.register(customUser,userModel)