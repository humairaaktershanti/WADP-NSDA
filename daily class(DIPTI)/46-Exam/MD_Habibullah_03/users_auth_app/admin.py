from django.contrib import admin
from users_auth_app.models import CustomUserModel,PendingAccountModel

admin.site.register(CustomUserModel)
admin.site.register( PendingAccountModel)