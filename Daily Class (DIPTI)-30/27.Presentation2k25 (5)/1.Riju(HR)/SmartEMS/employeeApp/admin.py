from django.contrib import admin
from employeeApp.models import *

# Register your models here.
admin.site.register(AttendanceModel)
admin.site.register(LeaveRequestModel)
admin.site.register(TaskModel)
admin.site.register(NotificationModel)
admin.site.register(TeamModel)
admin.site.register(TeamMemberModel)