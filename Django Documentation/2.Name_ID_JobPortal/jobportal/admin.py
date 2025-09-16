from django.contrib import admin
from .models import UserProfile, RecruiterProfile, JobSeekerProfile, JobPost, Application

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_type', 'display_name', 'created_at')
    list_filter = ('user_type', 'created_at')
    search_fields = ('user__username', 'display_name')

@admin.register(RecruiterProfile)
class RecruiterProfileAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'company_name', 'company_location')
    list_filter = ('company_location',)
    search_fields = ('company_name', 'user_profile__user__username')

@admin.register(JobSeekerProfile)
class JobSeekerProfileAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'has_resume')
    search_fields = ('user_profile__user__username', 'skills')
    
    def has_resume(self, obj):
        return bool(obj.resume)
    has_resume.boolean = True

@admin.register(JobPost)
class JobPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'recruiter', 'category', 'location', 'number_of_openings', 'posted_date', 'is_active')
    list_filter = ('category', 'location', 'is_active', 'posted_date')
    search_fields = ('title', 'description', 'recruiter__company_name')

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('job_post', 'job_seeker', 'applied_date', 'status')
    list_filter = ('status', 'applied_date')
    search_fields = ('job_post__title', 'job_seeker__user_profile__display_name')