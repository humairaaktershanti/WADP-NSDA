from django.shortcuts import render, redirect
from tasksApp.models import *

def Home(request):
    
    return render(request,'Home.html')


def AddTask(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        status = request.POST.get('status')
        due_date = request.POST.get('due_date')
        created_at = request.POST.get('created_at')
        
        new_task = To_DoModel(
            title=title,
            description=description,
            status=status,
            due_date=due_date,
            created_at=created_at
        )
        new_task.save()
        return redirect('TaskList')
        
        
    
    return render(request, 'AddTask.html')



def TaskList(request):
    tasks = To_DoModel.objects.all()
    context= {
        'Data': tasks
    }
    return render(request, 'TaskList.html', context)


def UpdateTask(request, id):
    task = To_DoModel.objects.get(id=id)
    
    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        task.status = request.POST.get('status')
        task.due_date = request.POST.get('due_date')
        task.created_at = request.POST.get('created_at')
        task.save()
        return redirect('TaskList')
    
    context = {
        'task': task
    }
    return render(request, 'UpdateTask.html', context)

def DeleteTask(request, id):
    task = To_DoModel.objects.get(id=id)
    task.delete()
    return redirect('TaskList')
 
    