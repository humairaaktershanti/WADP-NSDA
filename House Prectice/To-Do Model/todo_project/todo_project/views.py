from django.shortcuts import render


def home(R):
    return render(R,"home.html")


def addTask(R):
    return render(R,"addTask.html")


def taskList(R):
    return render(R,"taskList.html")
    