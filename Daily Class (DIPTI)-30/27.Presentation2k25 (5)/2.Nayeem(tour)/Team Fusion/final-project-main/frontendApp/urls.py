
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
        path('team/', team, name='team'),
        path('testimonials/', testimonials, name='testimonials'),
        path('404/', error_404_view, name='error_404'),
        path('become-a-guide/', become_guide, name='become_guide'),
        path('login/', frontend_login, name='frontend_login'),
        path('logout/', logout_view, name='logout'),
        path('signup/', frontend_signup, name='frontend_signup'),
        path('profile/', frontend_profile, name='frontend_profile'),


]