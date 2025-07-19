from django.shortcuts import render ,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from .models import CustomUserModel , PendingAccountModel
from candidate_app.models import CandidateProfileModel 
from employer_app.models import EmployerProfileModel , jobModel

def signup_page(request):
    if request.method == 'POST':
        user_type = request.POST.get('user_type')
        phone = request.POST.get('phone')
        username = request.POST.get('username')
        email = request.POST.get('email')

        if user_type == 'admin':
            CustomUserModel.objects.create_user(
                username=username,
                email=email,
                password=phone,
                phone=phone,
                user_type='admin'
            )
        
        elif user_type in ['employer', 'candidate']:
            PendingAccountModel.objects.create(
                username=username,
                email=email,
                phone=phone,
                user_type=user_type,
                pending_status='pending'
            )

        return redirect('login')

    return render(request, "signup.html")






def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home') 
        else:
            return render(request, 'login.html', {"messages": ["Invalid username or password."]})

    return render(request, 'login.html')

def logout_page(request):
    logout(request)
    return redirect('login')
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        user = request.user

        if check_password(current_password, user.password):
            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)
                return redirect('home')

    return render(request, 'change_password.html')

def accept_account(request, id):
    if request.method == 'POST':
        account = PendingAccountModel.objects.get(id=id)
        if account:
            user = CustomUserModel.objects.create_user(
                username=account.username,
                email=account.email,
                password=account.phone,
                phone=account.phone,
                user_type=account.user_type
            )
            if account.user_type == 'candidate':
                CandidateProfileModel.objects.create(
                    candidate_user=user,
                    full_name=account.username,
                    email=account.email,
                    phone=account.phone
                )
            elif account.user_type == 'employer':
                EmployerProfileModel.objects.create(
                    employer_user=user,
                    email=account.email,
                    phone=account.phone
                )
            account.delete()
        return redirect('home')
def reject_account(request, id):
    if request.method == 'POST':
        account = PendingAccountModel.objects.get(id=id)
        account.pending_status = 'rejected'
        account.save()
    return redirect('pending_accounts')
def pendindg_account(request):
    pending_accounts = PendingAccountModel.objects.all()
    return render(request, 'pendinhaccount.html', {'pending_accounts': pending_accounts})
def home(request):
    if request.user.is_authenticated:
        job = jobModel.objects.all()
        return render(request, 'home.html', {'user': request.user, 'jobs': job})
    
def profile(request):
    if request.user.is_authenticated:
        user = request.user
        if user.user_type == 'candidate':
            profile = CandidateProfileModel.objects.get(candidate_user=user)
        elif user.user_type == 'employer':
            profile = EmployerProfileModel.objects.get(employer_user=user)
        else:
            profile = None
        
        return render(request, 'profile.html', {'user': user, 'profile': profile})
    
    return redirect('login')
  