from django.shortcuts import render, redirect
from libraryApp.models import *

# Create your views here.

def home(req):
    return render (req,"home.html")


def addBook(req):

    if req.method=='POST':
        title=req.POST.get('title')
        author=req.POST.get('author')
        isbn=req.POST.get('isbn')
        coverImage=req.FILES.get('coverImage')
        publishedDate=req.POST.get('publishedDate')

        data=bookModel(
            title=title,
            author=author,
            isbn=isbn,
            coverImage=coverImage,
            publishedDate=publishedDate,

        )
        data.save()
        return redirect("listBook")
    return render (req,"addBook.html")


def listBook(req):
    data=bookModel.objects.all()
    context={
        'data':data
    }
    return render (req,"listBook.html",context)

def viewBook(req,id):
    data=bookModel.objects.get(id=id)
    context={
        'data':data
    }
    return render(req,"viewBook.html",context)

def deleteBook(req,id):
    data=bookModel.objects.get(id=id).delete()
    return redirect('listBook')


def editBook(req,id):
    data=bookModel.objects.get(id=id)

    context={
          'data':data
    }
    if req.method =='POST':
            data.id=id
            data.title=req.POST.get('title')
            data.author=req.POST.get('author')
            data.isbn=req.POST.get('isbn')
            if req.FILES.get('coverImage'):
               data.coverImage=req.FILES.get('coverImage')
            data.publishedDate=req.POST.get('publishedDate')

            data.save()
            return redirect("listBook")
    
    return render (req,"editBook.html",context)



