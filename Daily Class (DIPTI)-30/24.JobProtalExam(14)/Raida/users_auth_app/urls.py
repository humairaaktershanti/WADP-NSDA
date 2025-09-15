from django.urls import path
from users_auth_app.views import *


urlpatterns = [
    path('', registerPage, name='registerPage'),
    path('loginPage/', loginPage, name='loginPage'),

    path('changePasswordPage/', changePasswordPage, name='changePasswordPage'),
    path('dashboardPage/', dashboardPage, name='dashboardPage'),


    #pendingssss
    path('pendingAccount/', pendingAccount, name='pendingAccount'),
    path('approve_account/', approve_account, name='approve_account'),

    #logout
    path('logoutPage/', logoutPage, name='logoutPage'),

]
