from django.shortcuts import render
from storeApp.models import *

def home(req):
    return render(req,"home.html")

def books(req):
    bookdata=book.objects.all()
    context={

        'books': bookdata,
    }
    return render(req,"books.html", context)


def users(req):
    userdata=user.objects.all()
    context={

        'user': userdata,
    }
    return render(req,"user.html", context)