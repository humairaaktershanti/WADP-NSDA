from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import *

def logIn(req):
    if req.method=='POST':
        username = req.POST.get('username')
        password = req.POST.get('password')

        user = authenticate(req, username=username, password=password)

        if user is not None:
            login(req, user)
            return redirect('dashboard')
    return render(req, 'logIn.html')

def signUp(req):
    if req.method=='POST':
        username = req.POST.get('username')
        email = req.POST.get('email')
        password = req.POST.get('password')
        confirmPassword = req.POST.get('password2')
        
        if password == confirmPassword:
            user = AuthModel.objects.create_user(
                username = username,
                email = email,
                password = password,
                )
            newProfile=ProfileModel.objects.create(
                user=user
            )
            return redirect('logIn')
    return render(req, 'signUp.html')

@login_required(login_url='logIn')
def logOut(req):
    logout(req)
    return redirect('logIn')

@login_required(login_url='logIn')
def dashboard(req):
    return render(req, 'dashboard.html')

@login_required(login_url='logIn')
# def profile(req):
#     if req.method == 'POST':
#         form = ProfileForm(req.POST, instance=profile)
#         if form.is_valid():
#             profile = form.save(commit=False)
#             profile.user = req.user
#             profile.save()
#             return redirect('profile')
#     else:
#         form = ProfileForm(instance=profile)
#     return render(req, 'profile.html', {'form': form, 'profile': profile})

def profile(req):
    user_data = ProfileModel.objects.get(user = req.user)
    if req.method == 'POST':
        profile_form = ProfileForm(req.POST, instance=user_data)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('profile')
    else:
        profile_form = ProfileForm(instance=user_data)
        
    context = {
        'form': profile_form
    }
    
    return render(req, 'profile.html', context)