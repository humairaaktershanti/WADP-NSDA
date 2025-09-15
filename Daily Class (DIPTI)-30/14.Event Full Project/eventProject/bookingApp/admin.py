from django.contrib import admin

# Register your models here.
from bookingApp.models import *
admin.site.register(eventUserModel)
admin.site.register(eventBookingModel)