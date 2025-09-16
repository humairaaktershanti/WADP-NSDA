from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from backendApp.models import CustomUserModel,TravelerProfileModel ,GuideRequestModel
import random
import string

def frontend_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = CustomUserModel.objects.get(email=email)
        except CustomUserModel.DoesNotExist:
            messages.error(request, "Invalid email or password")
            return redirect('frontend_login')

        if user.user_type not in ['traveler', 'tourguide']:
            messages.error(request, "Admin users cannot login here")
            return redirect('frontend_login')

        user_auth = authenticate(request, username=user.username, password=password)
        if user_auth is not None:
            login(request, user_auth)
            return redirect('index')
        else:
            messages.error(request, "Invalid email or password")
            return redirect('frontend_login')

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('index')

def frontend_signup(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name') 
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        def random_string(length=4):
            return ''.join(random.choices(string.digits, k=length))

        username = f"{first_name}{random_string(4)}"


        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('frontend_signup')


        if CustomUserModel.objects.filter(email=email).exists():
            messages.error(request, "Email already exists. Please use a different email.")
            return redirect('frontend_signup')

        # Create new user
        user = CustomUserModel(username=username, email=email, first_name=first_name, last_name=last_name, user_type='traveler')
        user.set_password(password)
        user.save()
        TravelerProfileModel.objects.create(
            user_id=user,
            email=email,
            full_name=f"{first_name} {last_name}",
        )
        messages.success(request, "Account created successfully! Please login.")
        return redirect('frontend_login')

    return render(request, 'signup.html')

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def services(request):
    return render(request, 'service.html')
def contact(request):
    return render(request, 'contact.html')
def packages(request):
    return render(request, 'package.html')
def team(request):
    return render(request, 'team.html')
def testimonials(request):
    return render(request, 'testimonial.html')
def error_404_view(request, exception):
    return render(request, '404.html', status=404)

def become_guide(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        location = request.POST.get('location')
        experience_years = request.POST.get('experience_years') or 0
        languages = request.POST.get('languages')
        bio = request.POST.get('bio')
        license_number = request.POST.get('license_number')
        accept_terms = request.POST.get('accept_terms') == 'on'
        fb_link = request.POST.get('fb_link')
        instagram_link = request.POST.get('instagram_link')
        linkedin_link = request.POST.get('linkedin_link')

        photo = request.FILES.get('photo')
        nid = request.FILES.get('nid')
        passport = request.FILES.get('passport')
        driving_license = request.FILES.get('driving_license')

        guide_request = GuideRequestModel.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            location=location,
            experience_years=experience_years,
            languages=languages,
            bio=bio,
            license_number=license_number,
            accept_terms=accept_terms,
            fb_link=fb_link,
            instagram_link=instagram_link,
            linkedin_link=linkedin_link,
            photo=photo,
            nid=nid,
            passport=passport,
            driving_license=driving_license
        )
        messages.success(request, "Your application has been submitted successfully!")
        return redirect('index')
    return render(request, 'become_guide.html')
def frontend_profile(request):
    return render(request, 'profile.html')
