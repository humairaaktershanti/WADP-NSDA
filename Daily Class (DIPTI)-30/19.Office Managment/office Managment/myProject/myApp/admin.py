from django.contrib import admin
from myApp.models import *
# Register your models here.
admin.site.register(customUserModel)
admin.site.register(departmentModel)
admin.site.register(employeeModel)
admin.site.register(leaveModel)



# if req.method == 'POST':
#     leaveType = req.POST.get('leaveType')
#     fromDate = req.POST.get('fromDate')
#     toDate = req.POST.get('toDate')

#     UserData = employeeModel.objects.get(user=req.user)
#     if UserData.user.userTypes == 'Employee':
#         leaveModel.objects.create(
#             employee=UserData,
#             leaveType=leaveType,
#             fromDate=fromDate,
#             toDate=toDate,
#             status='Pending'
#         )
#         return redirect('adminDashboard')