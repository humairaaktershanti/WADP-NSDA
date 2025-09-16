from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import UserProfile, Skill, Experience, Education, Project, Testimonial, Contact
from .forms import (
    UserRegistrationForm, UserProfileForm, SkillForm, ExperienceForm, 
    EducationForm, ProjectForm, TestimonialForm, ContactForm
)

def home_view(request):
    # Get the first user profile (for demo purposes)
    try:
        user_profile = UserProfile.objects.first()
        user = user_profile.user
    except:
        user_profile = None
        user = None
    
    if user:
        skills = Skill.objects.filter(user=user)
        experiences = Experience.objects.filter(user=user)
        educations = Education.objects.filter(user=user)
        projects = Project.objects.filter(user=user, featured=True)
        testimonials = Testimonial.objects.filter(user=user)
    else:
        skills = experiences = educations = projects = testimonials = []
    
    context = {
        'user_profile': user_profile,
        'skills': skills,
        'experiences': experiences,
        'educations': educations,
        'projects': projects,
        'testimonials': testimonials,
    }
    return render(request, 'home.html', context)

def about_view(request):
    # Get the first user profile (for demo purposes)
    try:
        user_profile = UserProfile.objects.first()
        user = user_profile.user
    except:
        user_profile = None
        user = None
    
    if user:
        skills = Skill.objects.filter(user=user)
        experiences = Experience.objects.filter(user=user)
        educations = Education.objects.filter(user=user)
    else:
        skills = experiences = educations = []
    
    context = {
        'user_profile': user_profile,
        'skills': skills,
        'experiences': experiences,
        'educations': educations,
    }
    return render(request, 'about.html', context)

def projects_view(request):
    # Get the first user profile (for demo purposes)
    try:
        user_profile = UserProfile.objects.first()
        user = user_profile.user
    except:
        user_profile = None
        user = None
    
    if user:
        projects = Project.objects.filter(user=user)
    else:
        projects = []
    
    context = {
        'projects': projects,
    }
    return render(request, 'projects.html', context)

def project_detail_view(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    
    context = {
        'project': project,
    }
    return render(request, 'project_detail.html', context)

def contact_view(request):
    # Get the first user profile (for demo purposes)
    try:
        user_profile = UserProfile.objects.first()
    except:
        user_profile = None
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            if user_profile:
                contact.user = user_profile.user
            contact.save()
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')
    else:
        form = ContactForm()
    
    context = {
        'form': form,
        'user_profile': user_profile,
    }
    return render(request, 'contact.html', context)

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Account created for {user.username}! Please complete your profile.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out')
    return redirect('home')

@login_required
def dashboard_view(request):
    try:
        user_profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        user_profile = None
    
    skills = Skill.objects.filter(user=request.user)
    experiences = Experience.objects.filter(user=request.user)
    educations = Education.objects.filter(user=request.user)
    projects = Project.objects.filter(user=request.user)
    testimonials = Testimonial.objects.filter(user=request.user)
    contacts = Contact.objects.filter(user=request.user)
    
    context = {
        'user_profile': user_profile,
        'skills': skills,
        'experiences': experiences,
        'educations': educations,
        'projects': projects,
        'testimonials': testimonials,
        'contacts': contacts,
    }
    return render(request, 'dashboard.html', context)

@login_required
def profile_setup_view(request):
    try:
        user_profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        user_profile = UserProfile(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('dashboard')
    else:
        form = UserProfileForm(instance=user_profile)
    
    return render(request, 'profile_setup.html', {'form': form})

@login_required
def manage_skills_view(request):
    skills = Skill.objects.filter(user=request.user)
    
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.user = request.user
            skill.save()
            messages.success(request, 'Skill added successfully!')
            return redirect('manage_skills')
    else:
        form = SkillForm()
    
    context = {
        'skills': skills,
        'form': form,
    }
    return render(request, 'manage_skills.html', context)

@login_required
def edit_skill_view(request, skill_id):
    skill = get_object_or_404(Skill, id=skill_id, user=request.user)
    
    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, 'Skill updated successfully!')
            return redirect('manage_skills')
    else:
        form = SkillForm(instance=skill)
    
    return render(request, 'edit_skill.html', {'form': form, 'skill': skill})

@login_required
def delete_skill_view(request, skill_id):
    skill = get_object_or_404(Skill, id=skill_id, user=request.user)
    
    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Skill deleted successfully!')
        return redirect('manage_skills')
    
    return render(request, 'delete_skill.html', {'skill': skill})

@login_required
def manage_experiences_view(request):
    experiences = Experience.objects.filter(user=request.user)
    
    if request.method == 'POST':
        form = ExperienceForm(request.POST)
        if form.is_valid():
            experience = form.save(commit=False)
            experience.user = request.user
            experience.save()
            messages.success(request, 'Experience added successfully!')
            return redirect('manage_experiences')
    else:
        form = ExperienceForm()
    
    context = {
        'experiences': experiences,
        'form': form,
    }
    return render(request, 'manage_experiences.html', context)

@login_required
def edit_experience_view(request, experience_id):
    experience = get_object_or_404(Experience, id=experience_id, user=request.user)
    
    if request.method == 'POST':
        form = ExperienceForm(request.POST, instance=experience)
        if form.is_valid():
            form.save()
            messages.success(request, 'Experience updated successfully!')
            return redirect('manage_experiences')
    else:
        form = ExperienceForm(instance=experience)
    
    return render(request, 'edit_experience.html', {'form': form, 'experience': experience})

@login_required
def delete_experience_view(request, experience_id):
    experience = get_object_or_404(Experience, id=experience_id, user=request.user)
    
    if request.method == 'POST':
        experience.delete()
        messages.success(request, 'Experience deleted successfully!')
        return redirect('manage_experiences')
    
    return render(request, 'delete_experience.html', {'experience': experience})

@login_required
def manage_educations_view(request):
    educations = Education.objects.filter(user=request.user)
    
    if request.method == 'POST':
        form = EducationForm(request.POST)
        if form.is_valid():
            education = form.save(commit=False)
            education.user = request.user
            education.save()
            messages.success(request, 'Education added successfully!')
            return redirect('manage_educations')
    else:
        form = EducationForm()
    
    context = {
        'educations': educations,
        'form': form,
    }
    return render(request, 'manage_educations.html', context)

@login_required
def edit_education_view(request, education_id):
    education = get_object_or_404(Education, id=education_id, user=request.user)
    
    if request.method == 'POST':
        form = EducationForm(request.POST, instance=education)
        if form.is_valid():
            form.save()
            messages.success(request, 'Education updated successfully!')
            return redirect('manage_educations')
    else:
        form = EducationForm(instance=education)
    
    return render(request, 'edit_education.html', {'form': form, 'education': education})

@login_required
def delete_education_view(request, education_id):
    education = get_object_or_404(Education, id=education_id, user=request.user)
    
    if request.method == 'POST':
        education.delete()
        messages.success(request, 'Education deleted successfully!')
        return redirect('manage_educations')
    
    return render(request, 'delete_education.html', {'education': education})

@login_required
def manage_projects_view(request):
    projects = Project.objects.filter(user=request.user)
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
            messages.success(request, 'Project added successfully!')
            return redirect('manage_projects')
    else:
        form = ProjectForm()
    
    context = {
        'projects': projects,
        'form': form,
    }
    return render(request, 'manage_projects.html', context)

@login_required
def edit_project_view(request, project_id):
    project = get_object_or_404(Project, id=project_id, user=request.user)
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Project updated successfully!')
            return redirect('manage_projects')
    else:
        form = ProjectForm(instance=project)
    
    return render(request, 'edit_project.html', {'form': form, 'project': project})

@login_required
def delete_project_view(request, project_id):
    project = get_object_or_404(Project, id=project_id, user=request.user)
    
    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Project deleted successfully!')
        return redirect('manage_projects')
    
    return render(request, 'delete_project.html', {'project': project})

@login_required
def manage_testimonials_view(request):
    testimonials = Testimonial.objects.filter(user=request.user)
    
    if request.method == 'POST':
        form = TestimonialForm(request.POST, request.FILES)
        if form.is_valid():
            testimonial = form.save(commit=False)
            testimonial.user = request.user
            testimonial.save()
            messages.success(request, 'Testimonial added successfully!')
            return redirect('manage_testimonials')
    else:
        form = TestimonialForm()
    
    context = {
        'testimonials': testimonials,
        'form': form,
    }
    return render(request, 'manage_testimonials.html', context)

@login_required
def edit_testimonial_view(request, testimonial_id):
    testimonial = get_object_or_404(Testimonial, id=testimonial_id, user=request.user)
    
    if request.method == 'POST':
        form = TestimonialForm(request.POST, request.FILES, instance=testimonial)
        if form.is_valid():
            form.save()
            messages.success(request, 'Testimonial updated successfully!')
            return redirect('manage_testimonials')
    else:
        form = TestimonialForm(instance=testimonial)
    
    return render(request, 'edit_testimonial.html', {'form': form, 'testimonial': testimonial})

@login_required
def delete_testimonial_view(request, testimonial_id):
    testimonial = get_object_or_404(Testimonial, id=testimonial_id, user=request.user)
    
    if request.method == 'POST':
        testimonial.delete()
        messages.success(request, 'Testimonial deleted successfully!')
        return redirect('manage_testimonials')
    
    return render(request, 'delete_testimonial.html', {'testimonial': testimonial})

@login_required
def manage_contacts_view(request):
    contacts = Contact.objects.filter(user=request.user)
    
    context = {
        'contacts': contacts,
    }
    return render(request, 'manage_contacts.html', context)

@login_required
def delete_contact_view(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id, user=request.user)
    
    if request.method == 'POST':
        contact.delete()
        messages.success(request, 'Contact deleted successfully!')
        return redirect('manage_contacts')
    
    return render(request, 'delete_contact.html', {'contact': contact})