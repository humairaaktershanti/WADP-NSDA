from django.shortcuts import render,redirect
from recipeApp.models import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

def signupPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        confirmPassword=request.POST.get('confirmPassword')
        gender=request.POST.get('gender')
        age=request.POST.get('age')
        city=request.POST.get('city')
        country=request.POST.get('country')
        usertype=request.POST.get('usertype')
        
        if password == confirmPassword:
            user=Recipe_User.objects.create_user(username=username,password=password)
            user.email=email
            user.Gender=gender
            user.UserType=usertype
            user.City=city
            user.Age=age
            user.Country=country
            user.save()
            return redirect('signinPage')
        else:
            return redirect('signupPage')
    
    return render(request,'signup.html')

def signinPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        
        user=authenticate(username=username,password=password)
        
        if user:
            login(request,user)
            return redirect('dashboard')
        else:
            return redirect('signinPage')
        
    return render(request,'signin.html')

@login_required
def dashboard(request):
    
    return render(request,'dashboard.html')

def logoupPage(request):
    
    logout(request)
    return redirect('signinPage')

@login_required
def addrecipePage(request):
    if request.method=='POST':
        RecipeTitle=request.POST.get('RecipeTitle')
        Ingredients=request.POST.get('Ingredients')
        Instructions=request.POST.get('Instructions')
        
        PreparationTime=request.POST.get('PreparationTime')
        CookingTime=request.POST.get('CookingTime')
        RecipeTiTotalTimetle=request.POST.get('TotalTime')
        NutritionalInformation=request.POST.get('NutritionalInformation')
        TotalCalorie=request.POST.get('TotalCalorie')
        
        ReciTagspeTitle=request.POST.get('Tags')
        RecipeCategory=request.POST.get('RecipeCategory')
        DifficultyLevel=request.POST.get('DifficultyLevel')
        SampleImage=request.FILES.get('SampleImage')
        print(SampleImage)
        
        current_user = request.user
        
        addrecipeData=addRecipeModel(
            RecipeTitle=RecipeTitle,
            Ingredients=Ingredients,
            Instructions=Instructions,
            PreparationTime=PreparationTime,
            CookingTime=CookingTime,
            TotalTime=RecipeTiTotalTimetle,
            NutritionalInformation=NutritionalInformation,
            TotalCalorie=TotalCalorie,
            Tags=ReciTagspeTitle,
            RecipeCategory=RecipeCategory,
            DifficultyLevel=DifficultyLevel,
            SampleImage=SampleImage,
            Create_by=current_user,
        )
        addrecipeData.save()
        return redirect('recipelistPage')
    
    
    return render(request,'Chef/addrecipe.html')

@login_required
def recipelistPage(request):
    current_user = request.user
    current_usertype=request.user.UserType
    if current_usertype == 'Chef':
        recipedata=addRecipeModel.objects.filter(Create_by=current_user)
    else:
        recipedata=addRecipeModel.objects.all()
    recipedict={
        'recipedata':recipedata
    }
    
    return render(request,'recipelist.html',recipedict)

@login_required
def profileView(request):
    
    current_user = request.user
    profiledata=Recipe_User.objects.get(username=current_user)
    
    datadict ={
        'profiledata':profiledata
    }
    
    return render(request,'profile.html',datadict)

@login_required
def editrecipe(request,recipeid):
    recipedata = addRecipeModel.objects.get(id=recipeid)
    
    recipedict={
        'recipedata':recipedata
    }
    
    return render(request,'Chef/editrecipe.html',recipedict)

@login_required
def viewrecipe(request,recipeid):
    recipedata = addRecipeModel.objects.get(id=recipeid)
    recipedict={
        'recipedata':recipedata
    }
    
    return render(request,'viewrecipe.html',recipedict)

@login_required
def deleterecipe(request,recipeid):
    recipedata = addRecipeModel.objects.get(id=recipeid)
    recipedata.delete()
    
    return redirect('recipelistPage')

@login_required
def updaterecipePage(request):
    if request.method=='POST':
        recipeid=request.POST.get('recipeid')
        preimg=request.POST.get('preimg')
        
        RecipeTitle=request.POST.get('RecipeTitle')
        Ingredients=request.POST.get('Ingredients')
        Instructions=request.POST.get('Instructions')
        
        PreparationTime=request.POST.get('PreparationTime')
        CookingTime=request.POST.get('CookingTime')
        RecipeTiTotalTimetle=request.POST.get('TotalTime')
        NutritionalInformation=request.POST.get('NutritionalInformation')
        TotalCalorie=request.POST.get('TotalCalorie')
        
        ReciTagspeTitle=request.POST.get('Tags')
        RecipeCategory=request.POST.get('RecipeCategory')
        DifficultyLevel=request.POST.get('DifficultyLevel')
        SampleImage=request.FILES.get('SampleImage')
        print(SampleImage)
        
        current_user = request.user
        
        if SampleImage:
            addrecipeData=addRecipeModel(
                id=recipeid,
                RecipeTitle=RecipeTitle,
                Ingredients=Ingredients,
                Instructions=Instructions,
                PreparationTime=PreparationTime,
                CookingTime=CookingTime,
                TotalTime=RecipeTiTotalTimetle,
                NutritionalInformation=NutritionalInformation,
                TotalCalorie=TotalCalorie,
                Tags=ReciTagspeTitle,
                RecipeCategory=RecipeCategory,
                DifficultyLevel=DifficultyLevel,
                SampleImage=SampleImage,
                Create_by=current_user,
            )
        else:
            addrecipeData=addRecipeModel(
                id=recipeid,
                RecipeTitle=RecipeTitle,
                Ingredients=Ingredients,
                Instructions=Instructions,
                PreparationTime=PreparationTime,
                CookingTime=CookingTime,
                TotalTime=RecipeTiTotalTimetle,
                NutritionalInformation=NutritionalInformation,
                TotalCalorie=TotalCalorie,
                Tags=ReciTagspeTitle,
                RecipeCategory=RecipeCategory,
                DifficultyLevel=DifficultyLevel,
                SampleImage=preimg,
                Create_by=current_user,
            )
            
        
        addrecipeData.save()
        return redirect('recipelistPage')

    return redirect('recipelistPage')