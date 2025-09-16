from django.contrib import admin
from libraryApp.models import *

# Register your models here.
class Display_Library_User(admin.ModelAdmin):
    list_display = ['FullName','username','UserType']
    
admin.site.register(Llibrary_User,Display_Library_User)
