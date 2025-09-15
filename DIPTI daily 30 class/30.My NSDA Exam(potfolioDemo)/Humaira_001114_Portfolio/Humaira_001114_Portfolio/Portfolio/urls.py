from django.urls import path
from .views import *

urlpatterns = [
    path('', portfolio, name='portfolio'),
    path('logIn/', logIn, name='logIn'),
    path('SignUp/', SignUp, name='SignUp'),
    path('cv/', dashboard, name='cv'),
    path('dashboard/', update_profile, name='dashboard'),
    path('portfolio/', portfolio, name='portfolio'),
    path('logOut/', logOut, name='logOut'),
    
    path('contact/', contact, name='contact'),
    path('contact_view/', contact_view, name='contact_view'),
]