from django.contrib import admin
from ECommerceApp.models import *

# Register your models here.
class ECommerceUserDisplay(admin.ModelAdmin):
    list_display=['FullName','username','UserType']

admin.site.register(ECommerceUser,ECommerceUserDisplay)
admin.site.register(CustomerInfoModel)
admin.site.register(SellerInfoModel)
admin.site.register(ContactInfoModel)
admin.site.register(ProductModel)