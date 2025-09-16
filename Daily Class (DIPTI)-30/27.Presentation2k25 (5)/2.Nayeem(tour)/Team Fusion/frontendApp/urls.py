
from django.contrib import admin
from django.urls import path

from backendApp import views 
from .views import *


urlpatterns = [

        path('', index, name='index'),
        path('about/', about, name='about'),
        path('services/', services, name='services'),
        path('contact/', contact, name='contact'),
        path('packages/', packages, name='packages'),
        path('packages/<int:pk>/', package_detail, name='package_detail'),
        path('guides/', team, name='team'),
         path('guide/<int:pk>/', guide_detail, name='guide_detail'),
        path('destinations/', destinations, name='destinations'),
        path('tours/', tours, name='tours'),
          path('tour/<int:pk>/', tour_detail, name='tour_detail'),
        path('country/<str:name>/tours/', country_tours, name='country_tours'),
        path('city/<str:name>/tours/', city_tours, name='city_tours'),
        path('category/<str:name>/tours/', category_tours, name='category_tours'),
        path('testimonials/', testimonials, name='testimonials'),
        path('404/', error_404_view, name='error_404'),
        path('become-a-guide/', become_guide, name='become_guide'),
        path('login/', frontend_login, name='frontend_login'),
        path('logout/', logout_view, name='logout'),
        path('signup/', frontend_signup, name='frontend_signup'),
        path('profile/', frontend_profile, name='frontend_profile'),


]