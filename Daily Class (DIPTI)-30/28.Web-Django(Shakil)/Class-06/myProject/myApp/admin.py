from django.contrib import admin
from myApp.models import studentModel, teacherModel, managementModel, staffModel, libraryModel

# Register your models here.
admin.site.register(studentModel)
admin.site.register(teacherModel)
admin.site.register(managementModel)
admin.site.register(staffModel)
admin.site.register(libraryModel)