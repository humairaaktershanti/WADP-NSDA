from django.shortcuts import HttpResponse

def home(request):
    return HttpResponse("Welcome to Django Project.")

def about(request):
    return HttpResponse("This is about page.")

