from django.shortcuts import render
from django.shortcuts import render
from myApp.models import *

# Create your views here.
def Home(request):
    return render(request,'Home.html')

def AddResturent(request):

    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        openingHours = request.POST.get('openingHours')


        Resturent = ResturentModel (
            name=name,
            address=address,
            phone_number=phone_number,
            email=email,
            openingHours=openingHours,
            )
        Resturent.save()
        return render(request, 'AddResturent.html')



