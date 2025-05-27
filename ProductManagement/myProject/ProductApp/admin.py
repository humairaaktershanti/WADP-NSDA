from django.contrib import admin

# Register your models here.
from ProductApp.models import*

admin.site.register(productModel)
admin.site.register(customerModel)