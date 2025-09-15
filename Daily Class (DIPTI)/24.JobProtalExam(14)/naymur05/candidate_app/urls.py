from django.urls import path
from .views import application_list , add_applied_job

urlpatterns = [ 
    path('applications/', application_list, name='application_list'),
    path('apply-job/', add_applied_job, name='add_applied_job'),

]
