from django.shortcuts import render,redirect
from employer_app.models import *
from django.contrib import messages

# Create your views here.

def homePage(request):
    return render(request, 'homePage.html')

def create_employer_profile(request):
    if request.method == 'POST':
        company_name = request.POST.get('company_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        location = request.POST.get('location')
        about_company = request.POST.get('about_company')
        company_logo = request.FILES.get('company_logo')

        if EmployerProfileModel.objects.filter(employer_user=request.user).exists():
            messages.error(request, 'Profile already exists.')
            return redirect('dashboardPage')
        

        EmployerProfileModel.objects.create(
            employer_user=request.user,
            company_name=company_name,
            email=email,
            phone=phone,
            location=location,
            about_company=about_company,
            company_logo=company_logo
        )

        messages.success(request, 'Employer profile created successfully.')
        return redirect('dashboardPage')

    return render(request, 'profile.html')