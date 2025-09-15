from django.shortcuts import render, redirect
from .models import *
from .forms import *

# Create your views here.

def home(request):
    author_data = Author.objects.all()
    book_data = Book.objects.select_related('author').all()
    
    books = Book.objects.select_related('author').all()
    for book in books:
        print("OUtput is: ",book.title, book.author.name)
    
    context = {
        "author_data":author_data,
        "book_data":book_data,
    }
    
    return render(request,'home.html',context)

def author(request):
    if request.method == 'POST':
        author_form = authorForm(request.POST)
        if author_form.is_valid():
            author_form.save()
            return redirect(home)
    else:
        author_form = authorForm()
    context = {
        "author_form":author_form
    }
    return render(request,'author.html',context)

def book(request):
    if request.method == 'POST':
        book_form = bookForm(request.POST)
        if book_form.is_valid():
            book_form.save()
            return redirect(home)
    else:
        book_form = bookForm()
    context = {
        "book_form":book_form
    }
    return render(request,'book.html',context)
