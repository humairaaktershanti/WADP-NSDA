from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import UserProfile, Skill, Experience, Education, Project, Testimonial, Contact

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'title', 'email', 'location')
    search_fields = ('name', 'title', 'bio')

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'level', 'percentage')
    list_filter = ('level', 'user')
    search_fields = ('name',)

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('user', 'position', 'company', 'start_date', 'end_date', 'current')
    list_filter = ('current', 'start_date', 'user')
    search_fields = ('position', 'company')

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('user', 'degree', 'institution', 'field_of_study', 'start_date', 'end_date', 'current')
    list_filter = ('current', 'start_date', 'user')
    search_fields = ('degree', 'institution', 'field_of_study')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'status', 'featured', 'created_date')
    list_filter = ('status', 'featured', 'created_date', 'user')
    search_fields = ('title', 'description', 'technologies')

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'position', 'company')
    search_fields = ('name', 'company')

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'email', 'subject', 'created_at')
    list_filter = ('created_at', 'user')
    search_fields = ('name', 'email', 'subject')