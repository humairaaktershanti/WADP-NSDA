from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views
from AdminApp.views import admin_site_view, admin_login_view

from django.contrib.auth.views import LogoutView, PasswordChangeView, PasswordChangeDoneView

urlpatterns = [
    # Custom URLs should come before admin URLs
    path('', include('AuthApp.urls')),
    path('admin/', include('AdminApp.urls')),
    path('employee/', include('EmployeeApp.urls')),
    path('student/', include('StudentApp.urls')),
    
    # Django admin URLs should come last
    path('admin-panel/', admin_site_view, name='admin_panel'),
    path('admin/login/', admin_login_view, name='admin_login'),
    path('admin/logout/', auth_views.LogoutView.as_view(), name='admin_logout'),
    path('admin/password_change/', auth_views.PasswordChangeView.as_view(), name='admin_password_change'),
    path('admin/password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='admin_password_change_done'),
    path('admin/auth/group/', admin.site.urls),
    path('admin/AuthApp/user/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)