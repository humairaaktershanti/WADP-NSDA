from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile, User, oneModel, TwoModel, toDoModel
from .forms import ProfileForm, oneForm, twoForm

def index(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'index.html')

def logIn(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'login.html')

def SignUp(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return render(request, 'signup.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken')
            return render(request, 'signup.html')
        
        user = User.objects.create_user(username=username, email=email, password=password)
        Profile.objects.create(user=user)
        login(request, user)
        return redirect('logIn')
    
    return render(request, 'signup.html')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        
        if not request.user.check_password(current_password):
            messages.error(request, 'Current password is incorrect')
            return render(request, 'change_password.html')
        
        if new_password != confirm_password:
            messages.error(request, 'New passwords do not match')
            return render(request, 'change_password.html')
        
        request.user.set_password(new_password)
        request.user.save()
        messages.success(request, 'Password changed successfully')
        return redirect('dashboard')
    
    return render(request, 'change_password.html')

@login_required
def update_profile(request):
    profile = Profile.objects.get(user=request.user)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ProfileForm(instance=profile)
    
    return render(request, 'update_profile.html', {'form': form})

def logOut(request):
    logout(request)
    return redirect('index')

@login_required
def one(request):
    one, created = oneModel.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = oneForm(request.POST, request.FILES, instance=one)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = oneForm(instance=one)

    return render(request, 'one.html', {'form': form, 'value': 'Update One using form'})

@login_required
def two(request):
    if request.method == 'POST':
        form = twoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = twoForm()

    return render(request, 'two.html', {'form': form, 'value': 'Add Two using form'})

# [Done] CRUD [Worked]
@login_required
def addToDo(req):
    if req.method=='POST':
        title = req.POST.get('title')
        description = req.POST.get('description')
        status = req.POST.get('status')

        data = toDoModel(
            title=title,
            description=description,
            status=status
        )
        data.save()
        return redirect ('listToDo')
    return render(req,"addToDo.html")

@login_required
def listToDo(req):
    todo = toDoModel.objects.all()

    context={
        'todo':todo
    }
    return render(req,"listToDo.html",context)

@login_required
def deleteToDo(req, id):
    data = toDoModel.objects.get(id=id).delete()
    return redirect ('listToDo')

@login_required
def viewsToDo(req,id):
    data = toDoModel.objects.get(id=id)
    context={
        'data':data
    }
    return render(req,"viewsToDo.html", context)

@login_required
def updateToDo(req,id):
    data=toDoModel.objects.get(id=id)
    if req.method=='POST':
        data.id=id
        data.title=req.POST.get('title')
        data.description=req.POST.get('description')
        data.status=req.POST.get('status')

        data.save()
        return redirect ('listToDo')
    context={
        'data':data
    }

    return render(req, "updateToDo.html", context)