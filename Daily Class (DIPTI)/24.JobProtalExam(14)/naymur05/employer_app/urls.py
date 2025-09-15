from django.urls import path
from .views import job_list, add_job , delete_job , edit_job, view_job


urlpatterns = [
    path('jobs/', job_list, name='job_list'),
    path('add_job/', add_job, name='add_job'),
    path('delete_job/<int:id>/', delete_job, name='deletejob'),
    path('edit_job/<int:id>/', edit_job, name='editjob'),
    path('view_job/<int:id>/', view_job, name='viewjob'),
]