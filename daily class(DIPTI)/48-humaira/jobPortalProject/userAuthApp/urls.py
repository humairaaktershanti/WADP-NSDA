
from django.urls import path
from userAuthApp.views import *



urlpatterns = [
    path('home/',home,name='home'),
    path('signUp/',signUp,name='signUp'),
    path('',logIn,name='logIn'),
    path('pendingList/',pendingList,name='pendingList'),
    path('logOut/',logOut,name='logOut'), 
    path('acceptPending/<int:id>',acceptPending,name='acceptPending'), 
    path('rejectPending/<int:id>',rejectPending,name='rejectPending'), 
    path('profile/',profile,name='profile'), 
    path('editProfile/<int:id>',editProfile,name='editProfile'), 



    path('changePassword/<int:id>',changePassword,name='changePassword'),    

] 




