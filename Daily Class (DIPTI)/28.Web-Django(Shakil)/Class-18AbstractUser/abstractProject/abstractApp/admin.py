from django.contrib import admin
from abstractApp.models import *

# Register your models here.
class Display_User_List(admin.ModelAdmin):
    list_display=['username','UserType','DisplayName','Education']
    
admin.site.register(Custome_User,Display_User_List)
