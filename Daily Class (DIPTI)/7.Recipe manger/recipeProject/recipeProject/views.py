from django.shortcuts import render, redirect
from myApp.models import *


def home(req):
    return render(req,"home.html")



def addRecipe(req):

    if req.method=='POST':
        RecipeTitle=req.POST.get('RecipeTitle')
        RecipeImage=req.FILES.get('RecipeImage')
        Ingredients=req.POST.get('Ingredients')
        Instruction=req.POST.get('Instruction')
        Category=req.POST.get('Category')
        Description=req.POST.get('Description')

        data= recipeModel(
            RecipeTitle=RecipeTitle,
            RecipeImage=RecipeImage,
            Ingredients=Ingredients,
            Instruction=Instruction,
            Category=Category,
            Description=Description,

        )
        data.save()

        return redirect('RecipeList')



    return render(req,"addRecipe.html")


def RecipeList(req):

    data=recipeModel.objects.all()
    context={
        'data': data
    }

    return render(req,"RecipeList.html",context)


def deleteRecipe(req,id):

    data=recipeModel.objects.get(id=id).delete()

    return redirect('RecipeList')


def viewsRecipe(req,id):

    data=recipeModel.objects.get(id=id)
    context={
        'data': data
    }

    return render(req,"viewsRecipe.html",context)







def editRecipe(req,id):


    data=recipeModel.objects.get(id=id)
    context={
        'data':data
    }

    if req.method=='POST':
        RecipeTitle=req.POST.get('RecipeTitle')
        RecipeImage=req.FILES.get('RecipeImage')
        Ingredients=req.POST.get('Ingredients')
        Instruction=req.POST.get('Instruction')
        Category=req.POST.get('Category')
        Description=req.POST.get('Description')

        data= recipeModel(
            id=id,
            RecipeTitle=RecipeTitle,
            RecipeImage=RecipeImage,
            Ingredients=Ingredients,
            Instruction=Instruction,
            Category=Category,
            Description=Description,

        )
        data.save()

        return redirect('RecipeList')



    return render(req,"editRecipe.html",context)



