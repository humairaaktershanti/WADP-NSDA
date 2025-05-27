
from django.contrib import admin
from django.urls import path
from myProject.views import*

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home,name='home'),
    path('',products,name='products'),
    path('',addProduct,name='addProduct'),

]
