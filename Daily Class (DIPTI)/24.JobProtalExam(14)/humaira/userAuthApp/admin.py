from django.contrib import admin

# Register your models here.
from userAuthApp.models import *

admin.site.register(customUserModel)
admin.site.register(pendingAccountModel)