from django.contrib import admin

from .models import *


admin.site.register(CustomUserModel)
admin.site.register(TravelerProfileModel)
admin.site.register(AdminProfileModel)
admin.site.register(GuideProfile)
admin.site.register(GuideRequestModel)
admin.site.register(City)
admin.site.register(Country)
admin.site.register(TourCategory)
admin.site.register(Tour)
admin.site.register(Package)





