from django.contrib import admin
from adminApp.models import *

# Register your models here.
admin.site.register(DepartmentModel)
admin.site.register(DesignationModel)
admin.site.register(ProfileModel)
admin.site.register(HolidayModel)
admin.site.register(NoticeModel)
admin.site.register(PromotionModel)
admin.site.register(ResignationModel)
admin.site.register(TerminationModel)
admin.site.register(ActivityLogModel)