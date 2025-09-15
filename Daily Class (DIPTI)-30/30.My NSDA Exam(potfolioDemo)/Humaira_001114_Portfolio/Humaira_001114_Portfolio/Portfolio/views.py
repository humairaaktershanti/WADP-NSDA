from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile, User, Contact
from .forms import ProfileForm, ContactForm

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
    profile = Profile.objects.last()
    context = {
        'profile': profile,
    }
    return render(request, 'dashboard.html', context)


@login_required
def update_profile(request):
    profile = Profile.objects.get(user=request.user)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ProfileForm(instance=profile)
    
    return render(request, 'update_profile.html', {'form': form})

def logOut(request):
    logout(request)
    return redirect('portfolio')

def portfolio(request):
    profile = Profile.objects.last()
    context = {
        'profile': profile,
    }
    return render(request, 'portfolio.html', context)


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('portfolio')
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form, 'value': 'Send a message'})

def contact_view(request):
    contact = Contact.objects.all()
    context = {
        'contact': contact,
    }
    return render(request, 'contact_view.html', context)