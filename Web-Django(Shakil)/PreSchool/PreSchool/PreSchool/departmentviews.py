from django.shortcuts import render, redirect
from PreSchoolApp.models import *
from django.contrib import messages


#-----------Depeartment Section--------------------

def addDepartment(request):
    if request.method == 'POST':
        deptName = request.POST.get('deptName')
        deptHead = request.POST.get('deptHead')
        print("outside if")
        if DepartmentModel.objects.filter(department_name=deptName).exists():
            messages.warning(request,'Department already exist.')
            
        else:
            department = DepartmentModel(
                department_name=deptName,
                department_head_name=deptHead,
            )
            department.save()
            messages.success(request,'Department Successfully Created.')
            return redirect('departmentList')
    
    return render(request,'department/adddepartment.html')

def editDepartment(request,myid):
    departmentdata= DepartmentModel.objects.get(id=myid)
    
    contex = {
        'departmentdata':departmentdata,
    }
    
    if request.method == 'POST':
        deptid = request.POST.get('deptid')
        deptName = request.POST.get('deptName')
        deptHead = request.POST.get('deptHead')
        
        DepartmentModel.objects.filter(id=deptid).update(
            department_name=deptName,
            department_head_name=deptHead
        )
        messages.success(request,'Department Successfully Updated.')
        return redirect('departmentList')
    
    return render(request,'department/editdepartment.html',contex)

def deleteDepartment(request,myid):
    departmentdata= DepartmentModel.objects.get(id=myid)
    departmentdata.delete()
    return redirect('departmentList')
    
def departmentList(request):
    departmentdata= DepartmentModel.objects.all()
    
    contex = {
        'departmentdata':departmentdata,
    }
    
    return render(request,'department/departmentlist.html',contex)


def viewDepartment(request,myid):
    departmentdata= DepartmentModel.objects.get(id=myid)
    
    contex = {
        'departmentdata':departmentdata,
    }
    
    
    return render(request,'department/departmentlist.html',contex)

