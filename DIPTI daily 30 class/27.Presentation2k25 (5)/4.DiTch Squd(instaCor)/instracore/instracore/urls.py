from django.contrib import admin
from django.urls import path, include#, re_path
from django.conf import settings
from django.conf.urls.static import static

#from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('AuthApp.urls')),
    path('Admin/', include('AdminApp.urls', namespace='admin_dashboard')),
    path('employee/', include('EmployeeApp.urls')),
    path('student/', include('StudentApp.urls')),
    path('candidate/', include('CandidateApp.urls')),
]

# urlpatterns+=re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
# urlpatterns+=re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),