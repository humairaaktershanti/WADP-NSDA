from django.contrib import admin
from django.urls import path
from users_auth_app.views import*
urlpatterns = [
    path('register_page/',register_page, name="register_page"),
    path('',login_page, name="login_page"),
    path('home_page/',home_page,name="home_page"),
    path('logout_page/',logout_page,name="logout_page"),
    path('chnge_pass/',chnge_pass,name="chnge_pass"),
    path('panding_list/',panding_list,name="panding_list"),
    path('approveUser/<str:id>',approveUser,name="approveUser"),
    path('Reject/<str:id>',Reject,name="Reject"),


]
