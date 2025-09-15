from django.contrib import admin
from user_auth_app.models import *

admin.site.register(CustomUserModel)
admin.site.register(PendingAccountModel)