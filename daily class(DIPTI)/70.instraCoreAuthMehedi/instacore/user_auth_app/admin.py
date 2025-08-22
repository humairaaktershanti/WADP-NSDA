from django.contrib import admin
from user_auth_app.models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Notification)
admin.site.register(AuditLog)
admin.site.register(Trash)
admin.site.register(ActivityLog)