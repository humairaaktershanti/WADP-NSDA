from django.shortcuts import render,redirect
from users_auth_app.models import CustomUserModel,PendingAccountModel

from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate, login,logout
def user_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        user_types = request.POST.get('user_types')

        if user_types == 'Admin':
            CustomUserModel.objects.create_user(
                username=username,
                email=email,
                phone=phone,
                user_types='Admin',
                password=phone  
            )
            return redirect('login')
        else:
            PendingAccountModel.objects.create(
                username=username,
                email=email,
                phone=phone,
                user_types=user_types 
            )
            return redirect('login')

    return render(request, 'register.html')



def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username') 
        password = request.POST.get('password') 

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
      
    return render(request, 'login.html.html')

def logoutPage(request):
    logout(request)
    return redirect('dashboard')

@login_required
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')

        user = request.user
        if user.check_password(current_password):
            user.set_password(new_password)
            user.save()
            return redirect('login')

    return render(request, 'change_password.html')


@login_required
def DashboardPage(request):

    return render(request,'DashboardPage.html')




