from django.shortcuts import render, redirect
from myApp.models import *



# Create your views here.
def index(req):
    return render (req,'index.html')


def recipeCreate(req):
    if req.method=='POST':
        title = req.POST.get('title')
        description = req.POST.get('description')
        ingredients = req.POST.get('ingredients')
        instructions = req.POST.get('instructions')
        image = req.FILES.get('image')

        newRecipe=recipeModel(
            title=title,
            description=description,
            ingredients=ingredients,
            instructions=instructions,
            image=image,

        )
        newRecipe.save()
        return redirect ('recipeList')


    return render (req,'recipeCreate.html')


def recipeList(req):
    viewRecipe = recipeModel.objects.all()
    context={
        'data':viewRecipe
    }
    return render(req,'recipeList.html',context)


def deleteRecipe(req,id):
    delRecipe = recipeModel.objects.get(id=id).delete()
    
    return redirect('recipeList')

def ViewRecipe(req,id):
    viewRecipe = recipeModel.objects.get(id=id)
    context={
        'data':viewRecipe
    }
    return render(req,'ViewRecipe.html',context)


def editRecipe(req,id):
    data = recipeModel.objects.get(id=id)
    context={
        'data':data
    }
    if req.method=='POST':
        data.id=id
        data.title = req.POST.get('title')
        data.description = req.POST.get('description')
        data.ingredients = req.POST.get('ingredients')
        data.instructions = req.POST.get('instructions')
        if req.FILES.get('image'):
            data.image = req.FILES.get('image')

        data.save()
        return redirect('recipeList')


    return render(req,'editRecipe.html', context)



