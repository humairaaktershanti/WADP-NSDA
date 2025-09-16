from django.contrib import admin
from .models import UserProfile, ConsumedCalorie

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'age', 'gender', 'height', 'weight', 'bmr', 'daily_calorie_goal')
    list_filter = ('gender',)
    search_fields = ('user__username', 'name')

@admin.register(ConsumedCalorie)
class ConsumedCalorieAdmin(admin.ModelAdmin):
    list_display = ('user', 'item_name', 'calories', 'date', 'time')
    list_filter = ('date',)
    search_fields = ('user__username', 'item_name')