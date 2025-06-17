from django.shortcuts import render, redirect
from myApp.models import *

def homeList(req):
    recipeData=RecipeModel.objects.all()
    context={
        'recipeData': recipeData
    }
    return render(req,"homeList.html",context)



def addRecipe(req):
    if req.method=='POST':
        Title=req.POST.get('Title')
        Description=req.POST.get('Description')
        Ingredients=req.POST.get('Ingredients')
        Instructions=req.POST.get('Instructions')
        Image=req.FILES.get('Image')


        recipeData=RecipeModel(
            Title=Title,
            Description=Description,
            Ingredients=Ingredients,
            Instructions=Instructions,
            Image=Image

        )
        recipeData.save()

        return redirect("homeList")


    return render(req,"addRecipe.html")


def viewTask(req,id):

    
    return render(req,"viewTask.html")