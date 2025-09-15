from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from myApp.models import *

def index(req):
    return render(req, 'index.html')
def signUp(req):
    if req.method=='POST':
        username = req.POST.get('username')
        email = req.POST.get('email')
        userTypes = req.POST.get('userTypes')
        password = req.POST.get('password')
        confurmPassword = req.POST.get('confirm_password')

        
        if password == confurmPassword:
            user = customUserModel.objects.create_user(
                username = username,
                email = email,
                password = password,
                userTypes = userTypes, 
                )
            return redirect('logIn')
    return render(req, 'signUp.html')

def logIn(req):
    if req.method=='POST':
        username = req.POST.get('username')
        Password = req.POST.get('password')       
        user = authenticate(req, username=username, password=Password)        
        if user is not None:
            login(req, user)

            data=customUserModel.objects.get(username=username)
            if data.userTypes=='Admin':
                return redirect('adminDashboard')
            
            if data.userTypes=='Employee':
                return redirect('employeeDashboard')            
        
    return render(req, 'logIn.html')

def logOut(req):
    logout(req)
    return redirect('logIn')

def adminDashboard(req):
    data = leaveModel.objects.all()
    context={
        'data':data
    }
        
    return render(req,'adminDashboard.html',context)

def employeeDashboard(req):
    return render (req,'employeeDashboard.html')


def addEmployee(req): 
        if req.method=='POST':
            username = req.POST.get('username')
            password = req.POST.get('password')
            confurmPassword = req.POST.get('confirm_password')
            fullName = req.POST.get('fullName')
            email = req.POST.get('email')
            phone = req.POST.get('phone')
            departmentName = req.POST.get('departmentName')
            departmentDescribtion = req.POST.get('departmentDescribtion')
            position = req.POST.get('position')
            dateOfJoining = req.POST.get('dateOfJoining')
            profilePicture = req.FILES.get('profilePicture')

            if password == confurmPassword:
                user = customUserModel.objects.create_user(
                    username = username,
                    email = email,
                    password = password,
                    userTypes = 'Employee', 
                    )

            depData=departmentModel.objects.create(
                name=departmentName,
                describtion=departmentDescribtion
            )
            data = employeeModel.objects.create(
                user=user,
                fullName=fullName,
                phone=phone,
                department=depData,
                position=position,
                dateOfJoining=dateOfJoining,
                profilePicture=profilePicture
            )          
            return redirect ('listEmployee')    

        return render (req,'addEmployee.html') 

def listEmployee(req):    
    data = employeeModel.objects.all()
    context={
        'data':data
    }
    return render(req,"listEmployee.html",context)

def editEmployee(req,id):
    data=employeeModel.objects.get(id=id)
    context={
        'data':data
    }
    if req.method=='POST':
        data.id=id
        data.user=data.user
        data.department=data.department
        data.fullName=req.POST.get('fullName')
        data.phone=req.POST.get('phone')
        data.position=req.POST.get('position')
        data.dateOfJoining=req.POST.get('dateOfJoining')
        data.profilePicture=req.FILES.get('profilePicture')

        data.save()
        return redirect ('listEmployee')

    return render(req,"editEmployee.html",context)

def viewEmployee(req,id):
    data=employeeModel.objects.get(id=id)
    context={
        'data':data
    }
    return render(req,'viewEmployee.html',context)

def deleteEmployee(req,id):
    data = employeeModel.objects.get(id=id).delete()
    return redirect ('listEmployee')

def addLeave(req):
    if req.method == 'POST':
        leaveType = req.POST.get('leaveType')
        fromDate = req.POST.get('fromDate')
        toDate = req.POST.get('toDate')

        user = employeeModel.objects.get(user=req.user)

        leaveModel.objects.create(
            employee = user,
            leaveType = leaveType,
            fromDate = fromDate,
            toDate = toDate,
            status = 'Pending'
        )
        return redirect('employeeDashboard')
    return render(req, 'addLeave.html')

def approvedLeave(req,id):
    data=leaveModel.objects.get(id=id)
    data.status='Approved'
    data.save()    
    return redirect('adminDashboard')
    
def rejectedLeave(req,id):
    data=leaveModel.objects.get(id=id)
    data.status='Rejected'
    data.save()    
    return redirect('adminDashboard')