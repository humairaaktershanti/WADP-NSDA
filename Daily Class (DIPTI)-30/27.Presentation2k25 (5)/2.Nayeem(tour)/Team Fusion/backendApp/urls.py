
from django import views
from django.urls import path
from .views import *

urlpatterns = [

    path('dashboard',dashboard_page, name='admin_dashboard'),
    path('dashboard/login/', loginpage, name='dashboard_login'),
    path('dashboard/logout/', logout_view, name='dashboard_logout'),
    path('dashboard/guides/', guide_management, name='guide_management'),
    path("reject-guide/<int:guide_id>/", reject_guide, name="reject_guide"),
    path("accept-guide/<int:guide_id>/", accept_guide, name="accept_guide"),
    path('guide/edit/<int:guide_id>/', edit_guide, name='edit_guide'),
    path('guide/delete/<int:guide_id>/', delete_guide, name='delete_guide'),
    path('tour_list/', tour_list, name='tour_list'),
    path('tours/add/',add_tour, name='add_tour'),
    path('add-category/', add_category, name='add_category'),
    path('add-country/', add_country, name='add_country'),
    path('add-city/', add_city, name='add_city'),
    path('tours/edit/<int:tour_id>/', edit_tour, name='edit_tour'),
    path('tours/delete/<int:tour_id>/', delete_tour, name='delete_tour'),
    path('packages_list/', package_management, name='package_management'),
    path('packages/add/', add_package, name='add_package'),
    path('packages/edit/<int:pk>/', edit_package, name='edit_package'),
    path('packages/delete/<int:pk>/', delete_package, name='delete_package'),


]
