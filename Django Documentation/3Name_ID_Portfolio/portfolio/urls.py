from django.urls import path
from . import views

urlpatterns = [
    # Public views
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('projects/', views.projects_view, name='projects'),
    path('project/<int:project_id>/', views.project_detail_view, name='project_detail'),
    path('contact/', views.contact_view, name='contact'),
    
    # Authentication views
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard views
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('profile-setup/', views.profile_setup_view, name='profile_setup'),
    
    # Skill management
    path('manage-skills/', views.manage_skills_view, name='manage_skills'),
    path('edit-skill/<int:skill_id>/', views.edit_skill_view, name='edit_skill'),
    path('delete-skill/<int:skill_id>/', views.delete_skill_view, name='delete_skill'),
    
    # Experience management
    path('manage-experiences/', views.manage_experiences_view, name='manage_experiences'),
    path('edit-experience/<int:experience_id>/', views.edit_experience_view, name='edit_experience'),
    path('delete-experience/<int:experience_id>/', views.delete_experience_view, name='delete_experience'),
    
    # Education management
    path('manage-educations/', views.manage_educations_view, name='manage_educations'),
    path('edit-education/<int:education_id>/', views.edit_education_view, name='edit_education'),
    path('delete-education/<int:education_id>/', views.delete_education_view, name='delete_education'),
    
    # Project management
    path('manage-projects/', views.manage_projects_view, name='manage_projects'),
    path('edit-project/<int:project_id>/', views.edit_project_view, name='edit_project'),
    path('delete-project/<int:project_id>/', views.delete_project_view, name='delete_project'),
    
    # Testimonial management
    path('manage-testimonials/', views.manage_testimonials_view, name='manage_testimonials'),
    path('edit-testimonial/<int:testimonial_id>/', views.edit_testimonial_view, name='edit_testimonial'),
    path('delete-testimonial/<int:testimonial_id>/', views.delete_testimonial_view, name='delete_testimonial'),
    
    # Contact management
    path('manage-contacts/', views.manage_contacts_view, name='manage_contacts'),
    path('delete-contact/<int:contact_id>/', views.delete_contact_view, name='delete_contact'),
]