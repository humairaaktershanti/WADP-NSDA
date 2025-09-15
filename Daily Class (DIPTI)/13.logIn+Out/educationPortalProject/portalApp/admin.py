from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(CustomUser)
admin.site.register(TeacherModel)
admin.site.register(StudentBasicInModel)
admin.site.register(StudentEducationInfoModel)