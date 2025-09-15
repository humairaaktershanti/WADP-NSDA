from django.contrib import admin
from django.urls import path
from myProject.views import studentPage, techerPage, manaementPage, staffPage,libraryPage

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',studentPage, name='student'),
    path('teacherpage/',techerPage, name='teacher'),
    path('managementpage/',manaementPage, name='management'),
    path('staffpage/',staffPage, name='staff'),
    path('librarypage/',libraryPage, name='library'),
]
