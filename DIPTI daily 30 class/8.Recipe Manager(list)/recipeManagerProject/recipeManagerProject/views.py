from django.shortcuts import render,redirect
from myApp.models import *

def home(req):
    return render(req,"home.html")


def formRecipes(req):
    if req.method=='POST':
        Title=req.POST.get('Title')
        Description=req.POST.get('Description')
        Ingredients=req.POST.get('Ingredients')
        Instructions=req.POST.get('Instructions')
        Image=req.FILES.get('Image')

        data=recipeModel(
            Title=Title,
            Description=Description,
            Ingredients=Ingredients,
            Instructions=Instructions,
            Image=Image



        )
        data.save()
        return redirect('ListRecipes')

    return render(req,"formRecipes.html")



def ListRecipes(req):
    data=recipeModel.objects.all()
    context={
        'data':data
    }
    return render(req,"ListRecipes.html",context)


def viewsRecipe(req,id):
    data=recipeModel.objects.get(id=id)
    context={
        'data':data
    }
    return render(req,'viewsRecipe.html',context)


def deleteRecipe(req,id):
    data=recipeModel.objects.get(id=id).delete()
    return redirect ('ListRecipes')


# def editRecipe(req,id):

#     data=recipeModel.objects.get(id=id)
#     context={
#         'data':data
#     }
   
#     if req.method=='POST':
#         Title=req.POST.get('Title')
#         Description=req.POST.get('Description')
#         Ingredients=req.POST.get('Ingredients')
#         Instructions=req.POST.get('Instructions')


#         Image=req.FILES.get('Image')
    

#         data=recipeModel(
#             id=id,
#             Title=Title,
#             Description=Description,
#             Ingredients=Ingredients,
#             Instructions=Instructions,
#             Image=Image
#         )   



#         data.save()
#         return redirect('ListRecipes')

#     return render(req,"editRecipe.html",context)






def editRecipe(req,id):

    data=recipeModel.objects.get(id=id)
    context={
        'data':data
    }
   
    if req.method=='POST':
        data.Title=req.POST.get('Title')
        data.Description=req.POST.get('Description')
        data.Ingredients=req.POST.get('Ingredients')
        data.Instructions=req.POST.get('Instructions')


        if req.FILES.get('Image'):
            data.Image=req.FILES.get('Image')

        data.save()
        return redirect('ListRecipes')

    return render(req,"editRecipe.html",context)
