from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(CustomUserModel)
admin.site.register(AddcashModel)
admin.site.register(ExpenceModel)
admin.site.register(DailyTotalModel)