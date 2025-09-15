from django.contrib import admin
from django.urls import path
from myApp.views import*
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls), 

    path('',index,name='index'),
    path('adminDashboard/',adminDashboard,name='adminDashboard'),
    path('employeeDashboard/',employeeDashboard,name='employeeDashboard'),
    
    path('addEmployee/',addEmployee,name='addEmployee'),    
    path('listEmployee/',listEmployee,name='listEmployee'),

    path('addLeave/',addLeave,name='addLeave'),


    path('logIn/',logIn,name='logIn'),
    path('signUp/',signUp,name='signUp'),
    path('logOut/',logOut,name='logOut'),


    path('viewEmployee/<int:id>',viewEmployee,name='viewEmployee'),
    path('editEmployee/<int:id>',editEmployee,name='editEmployee'),
    path('deleteEmployee/<int:id>',deleteEmployee,name='deleteEmployee'),

    path('approvedLeave/<int:id>',approvedLeave,name='approvedLeave'),
    path('rejectedLeave/<int:id>',rejectedLeave,name='rejectedLeave'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
