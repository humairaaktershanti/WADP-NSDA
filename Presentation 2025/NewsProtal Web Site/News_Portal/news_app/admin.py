from django.contrib import admin
from news_app.models import *

admin.site.register(CustomUserModel)
admin.site.register(NewsModel)
admin.site.register(CategoryModel)