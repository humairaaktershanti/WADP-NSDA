from django.contrib import admin
from PreSchoolApp.models import *
# Register your models here.

class customeUserDisplay(admin.ModelAdmin):
    list_display = ['username','email','UserType']
    
    search_fields=["username","UserType",'email']
    
    fieldsets = [
        (
            "Users",
            {"fields":["username","email","UserType","password"]}
        )
    ]
    
admin.site.register(customeUser,customeUserDisplay)

class DisplayStudent(admin.ModelAdmin):
    list_display = ['FullName']    
    
admin.site.register(StudentModel,DisplayStudent)

class DisplayDepartment(admin.ModelAdmin):
    list_display = ['department_name','department_head_name','create_at','update_at']    
    
admin.site.register(DepartmentModel,DisplayDepartment)


class SessionYearModelClass(admin.ModelAdmin):
    list_display = ['StartSession','EndSession','create_at','update_at']
    
    search_fields=["StartSession","EndSession",'create_at','update_at']
    
    fieldsets = [
        (
            "Department",
            {"fields":["StartSession","EndSession"]}
        )
    ]
    
admin.site.register(SessionYearModel,SessionYearModelClass)

