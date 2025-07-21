
from django.urls import path
from userAuthApp.views import *



urlpatterns = [
    path('home/',home,name='home'),
    path('signUp/',signUp,name='signUp'),
    path('',logIn,name='logIn'),
    path('pendingList/',pendingList,name='pendingList'),
    path('logOut/',logOut,name='logOut'), 
    path('acceptPending/<int:id>',acceptPending,name='acceptPending'), 
    # path('acceptPending/<int:id>',acceptPending,name='acceptPending'), 



    path('changePassword/',changePassword,name='changePassword'),    

] 




