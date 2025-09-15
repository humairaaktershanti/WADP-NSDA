from django.shortcuts import render
from myApp.models import studentModel, teacherModel, managementModel, staffModel, libraryModel

def studentPage(request):
    student = studentModel.objects.all()
    stdDict = {
        'stddata':student
    }
    return render(request, 'studentpage.html', stdDict)

def techerPage(request):
    teacher = teacherModel.objects.all()
    tecDict = {
        'tecdata':teacher
    }
    return render(request, 'teacherpage.html',tecDict)

def manaementPage(request):
    management = managementModel.objects.all()
    manDict = {
        'mandata': management
    }
    return render(request, 'management.html',manDict)

def staffPage(request):
    staff = staffModel.objects.all()
    stafDict = {
        'stadata': staff
    }
    return render(request, 'staff.html', stafDict)

def libraryPage(request):
    library = libraryModel.objects.all()
    libraryDict = {
        'libdata': library
    }
    return render(request, 'library.html', libraryDict)

