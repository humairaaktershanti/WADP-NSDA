from django.contrib import admin
from django.urls import path
from myProject.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',candidatePage,name="candidatePage"),
    path('addcandidate/',addcandidate,name="addcandidate"),    
    path('updatecandidate/',updatecandidate,name="updatecandidate"),    
    path('deleteCandidate/<str:myid>',deleteCandidate,name="deleteCandidate"),    
    path('editCandidate/<str:myid>',editCandidate,name="editCandidate"),    
    path('viewCandidate/<str:myid>',viewCandidate,name="viewCandidate"),    
]
