from django.shortcuts import render
from myApp.models import *
def Home(request):
    return render(request, 'Home.html')

def Resturent(request):
    return render(request, 'Resturent.html')

def AddResturent(request):

    if request.method == 'POST':
        restaurantName = request.POST.get('restaurantName')
        restaurantAddress = request.POST.get('restaurantAddress')
        restaurantPhone = request.POST.get('restaurantPhone')
        

        # Create a new Restaurant object and save it to the database
        new_restaurant = Restaurant(
            name=restaurant_name,
            address=restaurant_address,
            phone=restaurant_phone,
            email=restaurant_email
        )
        new_restaurant.save()

        return render(request, 'AddResturent.html', {'message': 'Restaurant added successfully!'})
    

    return render(request, 'AddResturent.html')