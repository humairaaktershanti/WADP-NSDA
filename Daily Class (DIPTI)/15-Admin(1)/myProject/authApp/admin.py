from django.contrib import admin
from .views import *

admin.site.register(customUser)
admin.site.register(studentPendingModel)
admin.site.register(studentModel)
admin.site.register(teacherModel)
