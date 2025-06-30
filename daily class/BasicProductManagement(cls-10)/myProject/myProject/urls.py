
from django.contrib import admin
from django.urls import path
from myProject.views import*

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home,name='home'),
    path('products/',products,name='products'),
    path('addProduct/',addProduct,name='addProduct'),

]
