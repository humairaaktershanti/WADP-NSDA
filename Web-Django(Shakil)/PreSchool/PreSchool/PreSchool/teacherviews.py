from django.shortcuts import render, redirect

#-----------Teacher Section--------------------
def teacherDashboard(request):
    
    return render(request,'teachers/teacherdashboard.html')

def addTeacher(request):
    
    return render(request,'teachers/addteacher.html')

def editTeacher(request):
    
    return render(request,'teachers/editteacher.html')

def teacherDetails(request):
    
    return render(request,'teachers/teacherdetails.html')

def teacherList(request):
    
    return render(request,'teachers/teacherlist.html')
