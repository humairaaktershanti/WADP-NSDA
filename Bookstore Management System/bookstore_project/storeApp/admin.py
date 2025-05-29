from django.contrib import admin

# Register your models here.
from storeApp.models import book, user


admin.site.register(book)
admin.site.register(user)