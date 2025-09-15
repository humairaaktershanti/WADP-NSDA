from django.urls import path
from .views import signup_page , login_page , logout_page, home ,pendindg_account , accept_account, reject_account , change_password ,profile

urlpatterns = [
    path('signup/', signup_page, name='signup'),
    path('',login_page, name='login'),
    path('logout/', logout_page, name='logout'),
    path('change_password/', change_password, name='change_password'),
    path('home/', home, name='home'),
    path('pending_accounts/', pendindg_account, name='pending_accounts'),
    path('accept_account/<int:id>/', accept_account, name='accept_account'),
    path('reject_account/<int:id>/', reject_account, name='reject_account'),
    path('profile/', profile, name='profile'),

]