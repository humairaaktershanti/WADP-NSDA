from django.shortcuts import render

# Create your views here.
from books.models import *

def book_form(req):
    if req.method == 'POST':
        title=req.POST.get('title')
        author=req.POST.get('author')
        category=req.POST.get('category')
        publishDate=req.POST.get('publishDate')
        description=req.POST.get('description')
        Cover_Photo=req.FILES.get('Cover_Photo')
    
        huma=book(
            Title=title,
            Author=author,
            BookCategory=category,
            PublishDate=publishDate,
            Description=description,
            Cover_Photo=Cover_Photo
        )
        huma.save()
    return render(req,"books/book_form.html")

def book_list(req):
    BookData=book.objects.all()
    context = {
        'bookData':BookData
    }
    return render(req,"books/book_list.html",context)

def book_confirm_delete(req):
    return render(req,"books/book_confirm_delete.html")