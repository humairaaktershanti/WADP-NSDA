from multiprocessing import context
from urllib import request
from django.shortcuts import get_object_or_404, render ,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login, authenticate,logout ,update_session_auth_hash
from .models import *
import random
import string
from django.core.mail import send_mail
from django.utils.timezone import now




def loginpage(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = CustomUserModel.objects.get(email=email)
        if user.user_type == 'admin':
            if not user:
                messages.error(request, 'User with this email does not exist.')
                return redirect('dashboard_login')
            user_auth = authenticate(request, username=user.username, password=password)
            if user_auth is not None:
             login(request, user_auth)
            messages.success(request, 'Login successful!')
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid password. Please try again.')
            return redirect('dashboard_login')

    return render(request, 'auth/admin_login.html')


def dashboard_page(request):
    if request.user.is_authenticated:
        total_guides = GuideProfile.objects.count()
        total_tours = Tour.objects.count()
        total_packages = Package.objects.count()
        context = {
            'total_guides': total_guides,
            'total_tours': total_tours,
            'total_packages': total_packages
        }
        return render(request, 'admin_dashboard.html', context)
    else:
        messages.error(request, 'You need to log in first.')
        return redirect('dashboard_login')
def logout_view(request):
    user_type = None
    if request.user.is_authenticated:
        user_type = request.user.user_type 
    logout(request)
    if user_type == 'admin':
        return redirect('dashboard_login')
    

    
      #guide management


def guide_management(request):
    if request.user.is_authenticated and request.user.user_type == 'admin':
        guide_requests = GuideRequestModel.objects.filter(status='pending')
        accepted_guides = GuideProfile.objects.all() 
        context = {
            'guide_requests': guide_requests,
            'accepted_guides': accepted_guides
        }
        return render(request, 'guidelist.html', context)
    else:
        messages.error(request, 'You need to log in first.')
        return redirect('dashboard_login')
    
def reject_guide(request, guide_id):
    guide = get_object_or_404(GuideRequestModel, id=guide_id)

    if request.method == "POST":
        review_notes = request.POST.get("review_notes", "")
        guide.status = "rejected"
        guide.review_notes = review_notes
        guide.reviewed_at = now()
        guide.save()

        subject = "Guide Application Rejected"
        message = (
            f"Dear {guide.first_name} {guide.last_name},\n\n"
            f"Your guide application has been reviewed and unfortunately, it was rejected.\n\n"
            f"Reason: {review_notes}\n\n"
            f"Thank you for your interest.\n\n"
            f"Best regards,\nTour Guide Management Team"
        )
        send_mail(
            subject,
            message,
            None, 
            [guide.email],
            fail_silently=False,
        )

        messages.success(request, f"Guide {guide.first_name} {guide.last_name} has been rejected and notified via email.")

    return redirect("guide_management")


 

def accept_guide(request, guide_id):
    guide_request = get_object_or_404(GuideRequestModel, id=guide_id)

    if request.method == "POST":
        price_per_day = request.POST.get("price_per_day", "0.00")
        guide_request.status = "approved"
        guide_request.reviewed_at = now()
        guide_request.save()

        def random_string(length=4):
            return ''.join(random.choices(string.digits, k=length))

        username = f"{guide_request.first_name}{random_string(4)}"

        user = CustomUserModel.objects.create_user(
            username=username,
            email=guide_request.email,
            first_name=guide_request.first_name,
            last_name=guide_request.last_name,
            password=guide_request.phone,
            user_type='tourguide'
        )

        guide_profile = GuideProfile.objects.create(
            user_id=user,
            full_name=f"{guide_request.first_name} {guide_request.last_name}",
            phone=guide_request.phone,
            location=guide_request.location,
            experience_years=guide_request.experience_years,
            languages=guide_request.languages,
            bio=guide_request.bio,
            specialties=guide_request.specialties,
            license_number=guide_request.license_number,
            price_per_day=price_per_day,
            photo=guide_request.photo,
            nid=guide_request.nid,
            passport=guide_request.passport,
            driving_license=guide_request.driving_license,
            fb_link=guide_request.fb_link,
            instagram_link=guide_request.instagram_link,
            linkedin_link=guide_request.linkedin_link,
        )

        # Copy certifications
        for cert in guide_request.certifications.all():
            GuideCertification.objects.create(
                guide=guide_profile,
                name=cert.name,
                chr_image=cert.certificate_image
            )

        # Copy achievements
        for ach in guide_request.achievements.all():
            GuideAchievement.objects.create(
                guide=guide_profile,
                description=ach.name
            )

        # Send email
        subject = "Your Guide Application Has Been Accepted 🎉"
        message = (
            f"Dear {guide_request.first_name} {guide_request.last_name},\n\n"
            f"Congratulations! Your application as a tour guide has been accepted.\n\n"
            f"Here are your login credentials:\n"
            f"Email (Username): {guide_request.email}\n"
            f"Password: {guide_request.phone}\n\n"
            f"👉 Please change your password after your first login for security.\n\n"
            f"💰 Offered Price:\n"
            f"Your daily service price has been set to: ${price_per_day}\n\n"
            f"If you accept this offer, you can start working as an official guide on our platform.\n\n"
            f"Best regards,\nTour Guide Management Team"
        )
        send_mail(subject, message, None, [guide_request.email], fail_silently=False)
        messages.success(request, f"Guide {guide_request.first_name} {guide_request.last_name} has been accepted and notified via email.")

    return redirect("guide_management")


def edit_guide(request, guide_id):
    guide = get_object_or_404(GuideProfile, id=guide_id)

    if request.method == "POST":
        # Basic fields
        guide.full_name = request.POST.get('full_name', guide.full_name)
        guide.phone = request.POST.get('phone', guide.phone)
        guide.location = request.POST.get('location', guide.location)
        guide.experience_years = request.POST.get('experience_years', guide.experience_years)
        guide.languages = request.POST.get('languages', guide.languages)
        guide.bio = request.POST.get('bio', guide.bio)
        guide.specialties = request.POST.get('specialties', guide.specialties)
        guide.license_number = request.POST.get('license_number', guide.license_number)
        guide.price_per_day = request.POST.get('price_per_day', guide.price_per_day)
        guide.availability_status = request.POST.get('availability_status') == 'True'

        # Files
        for field in ['photo', 'nid', 'passport', 'driving_license']:
            if request.FILES.get(field):
                setattr(guide, field, request.FILES.get(field))

        guide.fb_link = request.POST.get('fb_link', guide.fb_link)
        guide.instagram_link = request.POST.get('instagram_link', guide.instagram_link)
        guide.linkedin_link = request.POST.get('linkedin_link', guide.linkedin_link)

        guide.save()

        # Certifications
        cert_ids = request.POST.getlist('cert_id[]')
        cert_names = request.POST.getlist('certification_name[]')
        cert_images = request.FILES.getlist('certification_image[]')

        for i, name in enumerate(cert_names):
            if not name.strip():
                continue
            cert_id = cert_ids[i] if i < len(cert_ids) and cert_ids[i] else None
            if cert_id:
                cert = GuideCertification.objects.filter(id=cert_id, guide=guide).first()
                if cert:
                    cert.name = name
                    if i < len(cert_images) and cert_images[i]:
                        cert.chr_image = cert_images[i]
                    cert.save()
            else:
                GuideCertification.objects.create(
                    guide=guide,
                    name=name,
                    chr_image=cert_images[i] if i < len(cert_images) else None
                )

        # Achievements
        ach_ids = request.POST.getlist('ach_id[]')
        ach_names = request.POST.getlist('achievement_name[]')

        for i, desc in enumerate(ach_names):
            if not desc.strip():
                continue
            ach_id = ach_ids[i] if i < len(ach_ids) and ach_ids[i] else None
            if ach_id:
                ach = GuideAchievement.objects.filter(id=ach_id, guide=guide).first()
                if ach:
                    ach.description = desc
                    ach.save()
            else:
                GuideAchievement.objects.create(
                    guide=guide,
                    description=desc
                )

        messages.success(request, "Guide updated successfully!")
        return redirect('guide_management')

    return render(request, 'guidelist.html', {'guide': guide})

# Delete Guide
def delete_guide(request, guide_id):
    guide = get_object_or_404(GuideProfile, id=guide_id)
    if request.method == 'POST':
        guide.delete()
        messages.success(request, f"{guide.full_name} has been deleted successfully.")
        return redirect('guide_management') 

         #end guide management

            #tour management

def tour_list(request):
    tours = Tour.objects.all().select_related('category', 'country', 'city')
    categories = TourCategory.objects.all()
    countries = Country.objects.all()
    cities = City.objects.all()
    return render(request, 'tour_management.html', {
        'tours': tours,
        'categories': categories,
        'countries': countries,
        'cities': cities,
    })




def add_tour(request):
    categories = TourCategory.objects.filter(is_active=True)
    countries = Country.objects.filter(is_active=True)
    cities = City.objects.filter(is_active=True)

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        category_id = request.POST.get('category')
        country_id = request.POST.get('country')
        city_id = request.POST.get('city')
        regular_price = request.POST.get('regular_price')
        offer_price = request.POST.get('offer_price') or None
        duration_days = request.POST.get('duration_days') or None
        is_featured = request.POST.get('is_featured') == 'True'
        is_active = request.POST.get('is_active') == 'True'
        featured_image = request.FILES.get('tour_featured_image')
        multi_images = request.FILES.getlist('tour_images')

        category = get_object_or_404(TourCategory, id=category_id)
        country = get_object_or_404(Country, id=country_id)
        city = get_object_or_404(City, id=city_id)

        tour = Tour.objects.create(
            title=title,
            description=description,
            category=category,
            country=country,
            city=city,
            regular_price=regular_price,
            offer_price=offer_price,
            duration_days=duration_days,
            is_featured=is_featured,
            is_active=is_active,
            tour_featured_image=featured_image
        )

        
        for img in multi_images:
            TourImage.objects.create(tour=tour, image=img)

        messages.success(request, "Tour added successfully!")
        return redirect('tour_list')

    context = {
        'categories': categories,
        'countries': countries,
        'cities': cities,
    }
    return render(request, 'add_tour.html', context)



def add_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        image = request.FILES.get('catalog_image')
        is_active = request.POST.get('is_active') == 'True'

        TourCategory.objects.create(
            name=name,
            catalog_image=image,
            is_active=is_active
        )
        messages.success(request, "Category added successfully!")
    return redirect('add_tour')


def add_country(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        image = request.FILES.get('catalog_image')
        is_active = request.POST.get('is_active') == 'True'

        Country.objects.create(
            name=name,
            catalog_image=image,
            is_active=is_active
        )
        messages.success(request, "Country added successfully!")
    return redirect('add_tour')



# Add City via Modal

def add_city(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        country_id = request.POST.get('country')
        image = request.FILES.get('catalog_image')
        is_active = request.POST.get('is_active') == 'True'

        country = get_object_or_404(Country, id=country_id)

        City.objects.create(
            name=name,
            country=country,
            catalog_image=image,
            is_active=is_active
        )
        messages.success(request, "City added successfully!")
    return redirect('add_tour')

def edit_tour(request, tour_id):
    tour = get_object_or_404(Tour, pk=tour_id)

    if request.method == "POST":
        tour.title = request.POST.get("title")
        tour.description = request.POST.get("description")
        tour.regular_price = request.POST.get("regular_price")
        tour.offer_price = request.POST.get("offer_price")
        tour.duration_days = request.POST.get("duration_days")

        category_id = request.POST.get("category")
        country_id = request.POST.get("country")
        city_id = request.POST.get("city")

        if category_id:
            tour.category = get_object_or_404(TourCategory, id=category_id)
        if country_id:
            tour.country = get_object_or_404(Country, id=country_id)
        if city_id:
            tour.city = get_object_or_404(City, id=city_id)
        if "tour_featured_image" in request.FILES:
            tour.tour_featured_image = request.FILES["tour_featured_image"]

        images = request.FILES.getlist("tour_images")
        for img in images:
            TourImage.objects.create(tour=tour, image=img)
        tour.is_active = request.POST.get("is_active") == "True"

        tour.save()
        messages.success(request, "Tour updated successfully ✅")
        return redirect("tour_list")

   



def delete_tour(request, tour_id):
    tour = get_object_or_404(Tour, pk=tour_id)
    if request.method == "POST":
        tour.delete()
        messages.success(request, f"Tour '{tour.title}' deleted successfully.")
        return redirect('tour_list')
    return render(request, 'backend/delete_tour.html', {'tour': tour})

       #end tour management

       #packagemanagement

def add_package(request):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        package_price = request.POST.get("package_price")
        offer_price = request.POST.get("offer_price")
        duration_days = request.POST.get("duration_days")
        max_persons = request.POST.get("max_persons")
        package_featured_image = request.FILES.get("package_featured_image")
        tour_ids = request.POST.getlist("tours[]")
        guide_ids = request.POST.getlist("guides[]")
        is_active = True if request.POST.get("is_active") == "on" else False
        is_featured = True if request.POST.get("is_featured") == "on" else False

        package = Package.objects.create(
            name=name,
            description=description,
            package_price=package_price,
            offer_price=offer_price or None,

            duration_days=duration_days or None,
            max_persons=max_persons or None,
            is_active=is_active,
            is_featured=is_featured,
            package_featured_image=package_featured_image
        )

        package.tours.set(tour_ids)
        package.guides.set(guide_ids)

        messages.success(request, "Package added successfully!")
        return redirect('package_management')

    # if GET request, just redirect
    return redirect('package_management')

def package_management(request):
    packages = Package.objects.all()
    tours = Tour.objects.all()
    guides = GuideProfile.objects.all()

    context = {
        'packages': packages,
        'tours': tours,
        'guides': guides,
    }
    return render(request, 'package_management.html', context)


def edit_package(request,pk):
    package = get_object_or_404(Package, id= pk)

    if request.method == "POST":
        package.name = request.POST.get("name")
        package.description = request.POST.get("description")
        package.package_price = request.POST.get("package_price")
        package.offer_price = request.POST.get("offer_price") or None
        package.duration_days = request.POST.get("duration_days") or None
        package.max_persons = request.POST.get("max_persons") or None
        package.is_active = request.POST.get("is_active") == "on"
        package.is_featured = request.POST.get("is_featured") == "on"
        if request.FILES.get("package_featured_image"):
            package.package_featured_image = request.FILES["package_featured_image"]

        tour_ids = request.POST.getlist("tours[]")
        guide_ids = request.POST.getlist("guides[]")

        package.tours.set(tour_ids)
        package.guides.set(guide_ids)
        package.save()

        messages.success(request, "Package updated successfully!")
        return redirect("package_management")

def delete_package(request, pk):
    package = get_object_or_404(Package, pk=pk)
    package.delete()
    messages.success(request, "Package deleted successfully!")
    return redirect('package_management')
