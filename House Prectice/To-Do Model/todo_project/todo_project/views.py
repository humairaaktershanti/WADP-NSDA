from django.shortcuts import render, redirect
from tasksApp.models import *


def home(R):
    return render(R,"home.html")


def addTask(R):
    if R.method == "POST":
        title = R.POST.get('title')
        description=R.POST.get('description')
        status = R.POST.get('status')
        due_date = R.POST.get('due_date')

        new_obj = ToDoModel(
            title = title,
            description = description,
            status = status,
            due_date = due_date,         
        )
        new_obj.save()

        return redirect(taskList)

    return render(R,"addTask.html")

def taskList(R):
    listData = ToDoModel.objects.all()
    context = {
        'listData': listData
    }

    return render(R,"taskList.html", context)

def deleteTask(req, id):
    deleteTask = ToDoModel.objects.get(id=id).delete()
    #deleteTask.delete()
    return redirect('taskList')

def editTask(req, id):
    editTask = ToDoModel.objects.get(id=id)
    context={
        'editTask': editTask      
    }

    return render (req, "editTask.html",context)

def viewTask(req, id):
    viewTask = ToDoModel.objects.get(id=id)
    context={
        'viewTask':viewTask      
    }
    return render (req, "viewTask.html",context)