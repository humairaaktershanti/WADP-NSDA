from django.contrib import admin
from myApp.models import *

admin.site.register(customUserModel)
admin.site.register(recruitersModel)
admin.site.register(jobModel)
admin.site.register(jobSeekersModel)
admin.site.register(jobApplicationModel)