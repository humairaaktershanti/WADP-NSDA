from django.contrib import admin
from django.urls import path
from LibraryApp.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls), 

    path('studentDashboard/',studentDashboard,name='studentDashboard'),
    path('librarianDashboard/',librarianDashboard,name='librarianDashboard'),

    path('studentProfile/',studentProfile,name='studentProfile'),
    path('librarianProfile/',librarianProfile,name='librarianProfile'), 

    path('addBook/',addBook,name='addBook'),
    path('listBok/',listBok,name='listBok'), 



    path('editBook/<int:id>',editBook,name='editBook'),
    path('deleteBook/<int:id>',deleteBook,name='deleteBook'),       

    path('',signUp,name='signUp'),
    path('logIn/',logIn,name='logIn'),
    path('logOut/',logOut,name='logOut'),
    path('changePassword/',changePassword,name='changePassword'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




