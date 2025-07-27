from django.contrib import admin
from users_auth_app.models import CustomUserModel, PendingAccountModel


# Register your models here.

admin.site.register(CustomUserModel)
admin.site.register(PendingAccountModel)



