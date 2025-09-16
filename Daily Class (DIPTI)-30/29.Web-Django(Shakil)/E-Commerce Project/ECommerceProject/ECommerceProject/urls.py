from django.contrib import admin
from django.urls import path
from ECommerceProject.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',signinPage,name='signinPage'),
    path('signupPage/',signupPage,name='signupPage'),
    path('dashboard/',dashboard,name='dashboard'),
    path('logoutPage/',logoutPage,name='logoutPage'),
    
    #-------Profile Url---------------
    path('profilePage/',profilePage,name='profilePage'),
    path('basicinfoPage/',basicinfoPage,name='basicinfoPage'),
    path('contactinfoPage/',contactinfoPage,name='contactinfoPage'),
    path('editprofilePage/',editprofilePage,name='editprofilePage'),
    
    #----------Product Url-----------------
    path('addProductPage/',addProductPage,name='addProductPage'),
    path('productlistPage/',productlistPage,name='productlistPage'),
    path('updateProduct/',updateProduct,name='updateProduct'),
    
    path('deleteproduct/<str:proid>',deleteproduct,name='deleteproduct'),
    path('viewProductPage/<str:proid>',viewProductPage,name='viewProductPage'),
    path('editProduct/<str:proid>',editProduct,name='editProduct'),
]
