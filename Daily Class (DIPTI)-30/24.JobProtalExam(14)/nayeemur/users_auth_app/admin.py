from django.contrib import admin
from users_auth_app.models import *

admin.site.register(CustomUser)
admin.site.register(PendingAccountModel)
