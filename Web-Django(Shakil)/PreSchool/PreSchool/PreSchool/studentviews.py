from django.shortcuts import render, redirect
from PreSchoolApp.models import *
from django.contrib import messages
from datetime import datetime


#-----------Student Section--------------------
def studentDashboard(request):
    
    return render(request,'students/studentdashboard.html')

def addStudent(request):
    departmentdata = DepartmentModel.objects.all()
    context = {
        'departmentdata':departmentdata,
    }
    if request.method == 'POST':
        fullname= request.POST.get('fullname')
        username= request.POST.get('username')
        studentid= request.POST.get('studentid')
        gender= request.POST.get('gender')
        dateofbirth= request.POST.get('dateofbirth')
        religion= request.POST.get('religion')
        mobile= request.POST.get('mobile')
        email= request.POST.get('email')
        password= request.POST.get('password')
        studentImage= request.FILES.get('studentImage')
        presentaddress= request.POST.get('presentaddress')
        permanentaddress= request.POST.get('permanentaddress')
        
        department= request.POST.get('department')
        section= request.POST.get('section')
        startsession= request.POST.get('startsession')
        endsession= request.POST.get('endsession')
        
        fathername= request.POST.get('fathername')
        fatheroccupation= request.POST.get('fatheroccupation')
        fathermobile= request.POST.get('fathermobile')
        
        mothername= request.POST.get('mothername')
        motheroccupation= request.POST.get('motheroccupation')
        mothermobile= request.POST.get('mothermobile')

        if customeUser.objects.filter(username=username).exists():
            messages.warning(request,'User already exist.')
        else:            
            studentuser = customeUser.objects.create_user(
                username=username,
                password=password,
                email = email,
                UserType = '3',
                )
            studentuser.save()
            
            studentData = StudentModel(
                user=studentuser,
                FullName=fullname,
                StudentID=studentid,
                Gender=gender,
                DateOB=dateofbirth,
                Religion=religion,
                Mobile=mobile,
                StudentImage=studentImage,
                PresentAddress=presentaddress,
                PermanentAddress=permanentaddress,
                
                Department=department,
                StartSession=startsession,
                EndSession=endsession,
                
                Section=section,
                
                FatherName=fathername,
                FatherOccupation=fatheroccupation,
                FatherMobile=fathermobile,
                
                MotherName=mothername,
                MotherOccupation=motheroccupation,
                MotherMobile=mothermobile,
            )
            studentData.save()
            messages.success(request,'Successfully Created.')
            return redirect('studentList') 
        
    return render(request,'students/addstudent.html',context)

def editStudent(request, myid):
    studentinfo = StudentModel.objects.get(id=myid)
    userdata = customeUser.objects.get(username=studentinfo.user)
    departmentdata = DepartmentModel.objects.all()
    
    date_of_birth = studentinfo.DateOB.isoformat() if studentinfo.DateOB else ''

    stddict = {
        'studentinfo': studentinfo,
        'userdata': userdata,
        'departmentdata': departmentdata,
        'date_of_birth': date_of_birth,
    }
    
    
    if request.method == 'POST':
        fullname= request.POST.get('fullname')
        username= request.POST.get('username')
        studentid= request.POST.get('studentid')
        gender= request.POST.get('gender')
        dateofbirth= request.POST.get('dateofbirth')
        religion= request.POST.get('religion')
        mobile= request.POST.get('mobile')
        email= request.POST.get('email')
        password= request.POST.get('password')
        studentImage= request.FILES.get('studentImage')
        presentaddress= request.POST.get('presentaddress')
        permanentaddress= request.POST.get('permanentaddress')
        
        department= request.POST.get('department')
        section= request.POST.get('section')
        startsession= request.POST.get('startsession')
        endsession= request.POST.get('endsession')
        
        fathername= request.POST.get('fathername')
        fatheroccupation= request.POST.get('fatheroccupation')
        fathermobile= request.POST.get('fathermobile')
        
        mothername= request.POST.get('mothername')
        motheroccupation= request.POST.get('motheroccupation')
        mothermobile= request.POST.get('mothermobile')
        
        StudentModel.objects.filter(id=myid).update(
            FullName = fullname,
            StudentID=studentid,
            Gender=gender,
            DateOB=dateofbirth,
            Religion=religion,
            Mobile=mobile,
            StudentImage=studentImage,
            PresentAddress=presentaddress,
            PermanentAddress=permanentaddress,
            
            Department=department,
            StartSession=startsession,
            EndSession=endsession,
            Section=section,
            
            FatherName=fathername,
            FatherOccupation=fatheroccupation,
            FatherMobile=fathermobile,
            
            MotherName=mothername,
            MotherOccupation=motheroccupation,
            MotherMobile=mothermobile,
        )
        messages.success(request,'Successfully Updated.')
        return redirect('studentList') 
    
    return render(request, 'students/editstudent.html', stddict)


def studentList(request):
    studentinfo = StudentModel.objects.all()
    
    
    stddict = {
        'studentinfo':studentinfo
    }
    
    
    return render(request,'students/studentlist.html',stddict)

def studentDetails(request,myid):
    studentinfo = StudentModel.objects.get(id=myid)
    userdata=customeUser.objects.get(username=studentinfo.user)
    
    departmentdata = DepartmentModel.objects.get(id=studentinfo.Department)
    
    stddict = {
        'studentinfo':studentinfo,
        'userdata':userdata,
        'departmentdata':departmentdata,
        
    }
    
    return render(request,'students/studentdetails.html',stddict)

def deleteStudent(request,myid):
    deletedata = StudentModel.objects.get(id=myid)
    customuser = deletedata.user
    userdata=customeUser.objects.get(username=customuser)
    deletedata.delete()
    userdata.delete()
    
    return redirect('studentList')