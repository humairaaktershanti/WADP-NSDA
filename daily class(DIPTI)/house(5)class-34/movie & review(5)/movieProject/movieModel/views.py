from django.shortcuts import render, redirect
from movieModel.models import *

# Create your views here.

def home(req):
    return render (req,"home.html")


def addMovie(req):

    if req.method=='POST':
        title=req.POST.get('title')
        genre=req.POST.get('genre')
        posterImage=req.FILES.get('posterImage')
        releaseDate=req.POST.get('releaseDate')

        data=movieModel(
            title=title,
            genre=genre,
            posterImage=posterImage,
            releaseDate=releaseDate,


        )
        data.save()
        return redirect("listMovie")
    return render (req,"addMovie.html")


def listMovie(req):
    data=movieModel.objects.all()
    context={
        'data':data
    }
    return render (req,"listMovie.html",context)

def viewMovie(req,id):
    data=movieModel.objects.get(id=id)
    context={
        'data':data
    }
    return render(req,"viewMovie.html",context)

def deleteMovie(req,id):
    data=movieModel.objects.get(id=id).delete()
    return redirect('listMovie')


def editMovie(req,id):
    data=movieModel.objects.get(id=id)

    context={
          'data':data
    }
    if req.method =='POST':
            data.id=id
            data.title=req.POST.get('title')
            data.genre=req.POST.get('genre')
            if req.FILES.get('posterImage'):
               data.posterImage=req.FILES.get('posterImage')
            data.releaseDate=req.POST.get('releaseDate')

            data.save()
            return redirect("listMovie")
    
    return render (req,"editMovie.html",context)



