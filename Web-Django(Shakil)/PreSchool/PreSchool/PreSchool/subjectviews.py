from django.shortcuts import render, redirect

#-----------Subject Section--------------------

def addSubject(request):
    
    return render(request,'subject/addsubject.html')

def editSubject(request):
    
    return render(request,'subject/editsubject.html')

def subjectList(request):
    
    return render(request,'subject/subjectlist.html')