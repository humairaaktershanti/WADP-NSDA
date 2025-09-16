from email.mime import image
from django.db import models 
from django.db.models import Avg ,Count
from django.contrib.auth.models import AbstractUser



class CustomUserModel(AbstractUser):
  USER_TYPE_CHOICES = (
      ('traveler', 'Traveler'),
      ('tourguide', 'Tour Guide'),
      ('admin', 'Admin'),
  )
  user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='traveler')

class AdminProfileModel(models.Model):
    user = models.OneToOneField(CustomUserModel, on_delete=models.CASCADE ,related_name='admin_profile')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

class TravelerProfileModel(models.Model):
    user_id = models.OneToOneField(CustomUserModel, on_delete=models.CASCADE, related_name='traveler_profile')
    full_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    gender_choices = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    gender = models.CharField(max_length=10, choices=gender_choices, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    address_line = models.TextField(blank=True, null=True)
    terms_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.full_name} - Traveler"




# -------------------------
# Guide Request (Application)
# -------------------------
class GuideRequestModel(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    gender_choices = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    # Basic info
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=20)
    location = models.CharField(max_length=255)
    experience_years = models.PositiveIntegerField(default=0)
    languages = models.CharField(max_length=255, help_text="Comma-separated list of languages")
    bio = models.TextField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=gender_choices, blank=True, null=True)

    # Achievements (optional, comma-separated list)
    specialties = models.TextField(blank=True, null=True, help_text="Comma-separated list of specialties")

    # Documents
    photo = models.ImageField(upload_to='guide_photos/', blank=True, null=True)
    nid = models.ImageField(upload_to='nid_photos/', blank=True, null=True)
    passport = models.ImageField(upload_to='passport_photos/', blank=True, null=True)
    driving_license = models.ImageField(upload_to='driving_license_photos/', blank=True, null=True)
    license_number = models.CharField(max_length=100, blank=True, null=True)

    # Status
    accept_terms = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    review_notes = models.TextField(blank=True, null=True)

    # Social links
    fb_link = models.URLField(max_length=255, blank=True, null=True)
    instagram_link = models.URLField(max_length=255, blank=True, null=True)
    linkedin_link = models.URLField(max_length=255, blank=True, null=True)

    # Timestamps
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.status}"


class Certification(models.Model):
    guide_request = models.ForeignKey(GuideRequestModel, on_delete=models.CASCADE, related_name='certifications')
    name = models.CharField(max_length=100, blank=True, null=True)
    certificate_image = models.ImageField(upload_to='certification_images/', blank=True, null=True)

    def __str__(self):
        return self.name if self.name else "Unnamed Certification"


class Achievement(models.Model):
    guide_request = models.ForeignKey(GuideRequestModel, on_delete=models.CASCADE, related_name='achievements')
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name if self.name else "Unnamed Achievement"




# -------------------------
# Approved Guide Profile
# -------------------------
class GuideProfile(models.Model):
    user_id = models.OneToOneField(CustomUserModel, on_delete=models.CASCADE, related_name='guide_profile')

    # Main info
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    location = models.CharField(max_length=255)
    experience_years = models.PositiveIntegerField(default=0)
    languages = models.CharField(max_length=255, help_text="Comma-separated list of languages")
    bio = models.TextField(blank=True, null=True)
    specialties = models.TextField(blank=True, null=True, help_text="Comma-separated list of specialties")

    # Docs
    photo = models.ImageField(upload_to='guide_photos/', blank=True, null=True)
    nid = models.ImageField(upload_to='nid_photos/', blank=True, null=True)
    passport = models.ImageField(upload_to='passport_photos/', blank=True, null=True)
    driving_license = models.ImageField(upload_to='driving_license_photos/', blank=True, null=True)
    license_number = models.CharField(max_length=100, blank=True, null=True)
    fb_link = models.URLField(max_length=255, blank=True, null=True)
    instagram_link = models.URLField(max_length=255, blank=True, null=True)
    linkedin_link = models.URLField(max_length=255, blank=True, null=True)
    # Booking info
    availability_status = models.BooleanField(default=True)
    price_per_day = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.full_name} - Guide"


class GuideCertification(models.Model):
    guide = models.ForeignKey(GuideProfile, on_delete=models.CASCADE, related_name='certifications')
    name = models.CharField(max_length=100)
    chr_image = models.ImageField(upload_to='certification_images/', blank=True, null=True)

    def __str__(self):
        return self.name

class GuideAchievement(models.Model):
    guide = models.ForeignKey(GuideProfile, on_delete=models.CASCADE, related_name='achievements')
    description = models.TextField()

    def __str__(self):
        return self.description[:50]

class TourCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    catalog_image = models.ImageField(upload_to='category_images/', blank=True, null=True)
    is_featured = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)
    catalog_image = models.ImageField(upload_to='country_images/', blank=True, null=True)
    is_featured = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
class City(models.Model):
    name = models.CharField(max_length=100, unique=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='cities')
    catalog_image = models.ImageField(upload_to='city_images/', blank=True, null=True)
    is_featured = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('name', 'country')

    def __str__(self):
        return f"{self.name}, {self.country.name}"



class Tour(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.ForeignKey(TourCategory, on_delete=models.CASCADE, related_name='tours')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='tours')
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='tours')
    regular_price = models.DecimalField(max_digits=10, decimal_places=2)
    offer_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tour_featured_image = models.ImageField(upload_to='tour_featured_images/', blank=True, null=True)
    duration_days = models.PositiveIntegerField(null=True, blank=True)
    is_featured = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    @property
    def offer_percentage(self):
        if self.offer_price and self.regular_price > 0 and self.offer_price < self.regular_price:
            discount = self.regular_price - self.offer_price
            return round((discount / self.regular_price) * 100, 2)
        return 0

    @property
    def average_rating(self):
        review_stats = self.reviews.aggregate(avg=Avg('rating'))
        return round(review_stats['avg'] or 0, 1)

    @property
    def review_count(self):
        stats = self.reviews.aggregate(count=Count('id'))
        return stats['count'] or 0
    
class TourImage(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='tour_images/')

    def __str__(self):
        return f"Image for {self.tour.title}"
class TourReview(models.Model):
    tour = models.ForeignKey(Tour, related_name="reviews", on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()  # 1 to 5
    comment = models.TextField(blank=True, null=True)


class Package(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    tours = models.ManyToManyField(Tour, related_name='packages')
    guides = models.ManyToManyField(GuideProfile, related_name='packages', null=True, blank=True)
    package_price = models.DecimalField(max_digits=10, decimal_places=2)
    package_featured_image = models.ImageField(upload_to='package_featured_images/', blank=True, null=True)
    offer_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    duration_days = models.PositiveIntegerField(null=True, blank=True)
    max_persons = models.PositiveIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    @property
    def offer_percentage(self):
        if self.offer_price and self.package_price > 0 and self.offer_price < self.package_price:
            discount = self.package_price - self.offer_price
            return round((discount / self.package_price) * 100, 2)
        return 0
    



