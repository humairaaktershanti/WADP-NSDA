# settings.py

# INSTALLED_APPS = [
#     '...',
#     'authApp',
# ]

LOGIN_URL = 'logIn'

AUTH_USER_MODEL = 'authApp.User'

# urls.py

from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('authApp.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)