from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import views as auth_views
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

@staff_member_required
def admin_site_view(request):
    """
    Custom admin site view that checks if the user is a superuser
    """
    if not request.user.is_superuser:
        return render(request, 'AdminApp/admin_access_denied.html')
    
    # If the user is a superuser, redirect to the actual admin site
    return admin.site.index()

# Custom admin login view
def admin_login_view(request, **kwargs):
    """
    Custom admin login view that only allows superusers
    """
    response = auth_views.LoginView.as_view(**kwargs)(request)
    
    # After successful login, check if the user is a superuser
    if request.user.is_authenticated and not request.user.is_superuser:
        from django.contrib.auth import logout
        logout(request)
        return render(request, 'AdminApp/admin_access_denied.html')
    
    return response