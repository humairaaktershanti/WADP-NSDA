from django.contrib import admin

# Register your models here.
from .views import *

admin.site.register(customUser)
admin.site.register(toDoModel)
