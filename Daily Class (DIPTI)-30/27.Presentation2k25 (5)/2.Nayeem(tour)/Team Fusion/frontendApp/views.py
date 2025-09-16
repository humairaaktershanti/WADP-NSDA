from multiprocessing import context
from urllib import request
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from backendApp.models import Certification, City, Country, CustomUserModel, GuideProfile, Package, Achievement, Tour, TourCategory,TravelerProfileModel ,GuideRequestModel
import random
import string
from django.db.models import Count,Avg , Q
from django.core.paginator import Paginator

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
    countries = Country.objects.filter(is_featured=True, is_active=True).annotate(total_tours=Count('tours'))[:4]
    tours = Tour.objects.filter(is_featured=True, is_active=True).order_by('-id')[:6]
    packages = Package.objects.filter(is_featured=True, is_active=True).order_by('-id')[:6]
    guides = GuideProfile.objects.filter(availability_status=True)[:6]
    tour = Tour.objects.filter(is_featured=True, is_active=True).order_by('-id')


    context = {
        'countries': countries,
        'tours': tours,
        'packages': packages,
        'guides': guides,
        'tour' : tour
    }
    return render(request, 'index.html', context)

def about(request):
    return render(request, 'about.html')

def services(request):
    return render(request, 'service.html')
def contact(request):
    return render(request, 'contact.html')
def packages(request):
    packages = Package.objects.filter(is_active=True)
    paginator = Paginator(packages, 9)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'package.html', {'page_obj': page_obj})
def package_detail(request, pk):
    package = get_object_or_404(Package, pk=pk)
    return render(request, "package_detail.html", {
        "package": package,
        "traveler_range": range(1, 11),
    })


def team(request):
    guides = GuideProfile.objects.filter(availability_status=True)
    paginator = Paginator(guides, 9)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'team.html', {'page_obj': page_obj})


def guide_detail(request, pk):
    guide = get_object_or_404(GuideProfile, pk=pk)

    languages = guide.languages.split(",") if guide.languages else []
    specialties = guide.specialties.split(",") if guide.specialties else []

    return render(request, "guide_detail.html", {
        "guide": guide,
        "languages": [lang.strip() for lang in languages],
        "specialties": [sp.strip() for sp in specialties],
    })
def destinations(request):
    # Get only active countries and annotate tour count
    countries = Country.objects.filter(is_active=True).annotate(
        total_tours=Count('tours', filter=Q(tours__is_active=True))
    )
    cities = City.objects.filter(is_active=True).annotate(
        total_tours=Count('tours', filter=Q(tours__is_active=True))
    )

    # Categories with active tours
    categories = TourCategory.objects.filter(is_active=True).annotate(
        total_tours=Count('tours', filter=Q(tours__is_active=True))
    )

    # Paginate 8 per page
    paginator = Paginator(countries, 8)
    page_obj = paginator.get_page(request.GET.get('page'))
    
    return render(request, 'destination.html', {
        'page_obj': page_obj,
        'cities': cities,
        'categories': categories,
    })

def tours(request):
    tours = Tour.objects.filter(is_active=True)
    paginator = Paginator(tours, 9)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'tour_list.html', {'page_obj': page_obj})

def tour_detail(request, pk):
    tour = get_object_or_404(Tour, pk=pk, is_active=True)
    context = {
        "tour": tour,
    }
    return render(request, "tour_detail.html", context)

def country_tours(request, name):
    country=Country.objects.get(name=name)
    tours = Tour.objects.filter(is_active=True, country=country)
    paginator = Paginator(tours, 9)
    page_obj = paginator.get_page(request.GET.get('page'))
    country = Country.objects.get(name=name)
    return render(request, 'tour_list.html', {'page_obj': page_obj, 'country': country})
def city_tours(request, name):
    tours = Tour.objects.filter(is_active=True, city=name)
    paginator = Paginator(tours, 9)
    page_obj = paginator.get_page(request.GET.get('page'))
    city = City.objects.get(name=name)
    return render(request, 'tour_list.html', {'page_obj': page_obj, 'city': city})

def category_tours(request, name):
    category = get_object_or_404(TourCategory, name=name)
    tours = Tour.objects.filter(category=category, is_active=True)
    paginator = Paginator(tours, 9)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'tour_list.html', {'page_obj': page_obj, 'title': category.name})



def testimonials(request):
    return render(request, 'testimonial.html')
def error_404_view(request, exception):
    return render(request, '404.html', status=404)

def become_guide(request):
    if request.method == "POST":
        guide_request = GuideRequestModel.objects.create(
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            location=request.POST.get('location'),
            experience_years=request.POST.get('experience_years') or 0,
            languages=request.POST.get('languages'),
            bio=request.POST.get('bio'),
            specialties=request.POST.get('specialties') or None,
            license_number=request.POST.get('license_number'),
            gender=request.POST.get('gender') or None,
            accept_terms=True,
            fb_link=request.POST.get('fb_link'),
            instagram_link=request.POST.get('instagram_link'),
            linkedin_link=request.POST.get('linkedin_link'),
            photo=request.FILES.get('photo'),
            nid=request.FILES.get('nid'),
            passport=request.FILES.get('passport'),
            driving_license=request.FILES.get('driving_license')
        )

        # Save Certifications
        cert_names = request.POST.getlist('certification_name[]')
        cert_images = request.FILES.getlist('certification_image[]')
        for idx, name in enumerate(cert_names):
            Certification.objects.create(
                guide_request=guide_request,
                name=name,
                certificate_image=cert_images[idx] if idx < len(cert_images) else None
            )

        # Save Achievements
        achievement_names = request.POST.getlist('achievement_name[]')
        for name in achievement_names:
            Achievement.objects.create(
                guide_request=guide_request,
                name=name
            )

        messages.success(request, "Your application has been submitted successfully!")
        return redirect('index')

    return render(request, 'become_guide.html')




def frontend_profile(request):
    return render(request, 'profile.html')
