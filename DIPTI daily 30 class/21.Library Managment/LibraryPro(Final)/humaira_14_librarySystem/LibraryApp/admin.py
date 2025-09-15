from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(customUserModel)
admin.site.register(librarianProfileModel)  
admin.site.register(studentProfileModel) 
admin.site.register(bookModel) 
