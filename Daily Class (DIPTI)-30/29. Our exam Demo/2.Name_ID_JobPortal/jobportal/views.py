from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .forms import (
    UserRegistrationForm, UserProfileForm, RecruiterProfileForm, 
    JobSeekerProfileForm, ResumeUploadForm, JobPostForm, ApplicationForm
)
from .models import UserProfile, RecruiterProfile, JobSeekerProfile, JobPost, Application

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user_profile = UserProfile.objects.create(
                user=user,
                display_name=form.cleaned_data['display_name'],
                user_type=form.cleaned_data['user_type']
            )
            messages.success(request, f'Account created for {user.username}! Please complete your profile.')
            return redirect('profile_setup')
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
    return redirect('login')

@login_required
def profile_setup_view(request):
    try:
        user_profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user)
    
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, instance=user_profile)
        
        if user_profile.user_type == 'recruiter':
            recruiter_profile, created = RecruiterProfile.objects.get_or_create(user_profile=user_profile)
            recruiter_form = RecruiterProfileForm(request.POST, instance=recruiter_profile)
            if profile_form.is_valid() and recruiter_form.is_valid():
                profile_form.save()
                recruiter_form.save()
                messages.success(request, 'Your profile has been updated!')
                return redirect('dashboard')
        else:
            job_seeker_profile, created = JobSeekerProfile.objects.get_or_create(user_profile=user_profile)
            job_seeker_form = JobSeekerProfileForm(request.POST, instance=job_seeker_profile)
            if profile_form.is_valid() and job_seeker_form.is_valid():
                profile_form.save()
                job_seeker_form.save()
                messages.success(request, 'Your profile has been updated!')
                return redirect('dashboard')
    else:
        profile_form = UserProfileForm(instance=user_profile)
        
        if user_profile.user_type == 'recruiter':
            recruiter_profile, created = RecruiterProfile.objects.get_or_create(user_profile=user_profile)
            recruiter_form = RecruiterProfileForm(instance=recruiter_profile)
            return render(request, 'recruiter_profile_setup.html', {
                'profile_form': profile_form,
                'recruiter_form': recruiter_form
            })
        else:
            job_seeker_profile, created = JobSeekerProfile.objects.get_or_create(user_profile=user_profile)
            job_seeker_form = JobSeekerProfileForm(instance=job_seeker_profile)
            return render(request, 'job_seeker_profile_setup.html', {
                'profile_form': profile_form,
                'job_seeker_form': job_seeker_form
            })

@login_required
def dashboard_view(request):
    user_profile = request.user.userprofile
    
    if user_profile.user_type == 'recruiter':
        try:
            recruiter_profile = user_profile.recruiterprofile
            job_posts = JobPost.objects.filter(recruiter=recruiter_profile)
            applications = Application.objects.filter(job_post__recruiter=recruiter_profile)
            
            context = {
                'recruiter_profile': recruiter_profile,
                'job_posts': job_posts,
                'applications': applications,
            }
            return render(request, 'recruiter_dashboard.html', context)
        except RecruiterProfile.DoesNotExist:
            return redirect('profile_setup')
    else:
        try:
            job_seeker_profile = user_profile.jobseekerprofile
            applications = Application.objects.filter(job_seeker=job_seeker_profile)
            
            # Get job recommendations based on skills
            user_skills = [skill.strip().lower() for skill in job_seeker_profile.skills.split(',')]
            recommended_jobs = []
            
            for job in JobPost.objects.filter(is_active=True):
                job_skills = [skill.strip().lower() for skill in job.required_skills.split(',')]
                match_count = sum(1 for skill in user_skills if skill in job_skills)
                if match_count > 0:
                    recommended_jobs.append((job, match_count))
            
            # Sort by match count
            recommended_jobs.sort(key=lambda x: x[1], reverse=True)
            recommended_jobs = [job for job, _ in recommended_jobs[:5]]
            
            context = {
                'job_seeker_profile': job_seeker_profile,
                'applications': applications,
                'recommended_jobs': recommended_jobs,
            }
            return render(request, 'job_seeker_dashboard.html', context)
        except JobSeekerProfile.DoesNotExist:
            return redirect('profile_setup')

@login_required
def post_job_view(request):
    user_profile = request.user.userprofile
    
    if user_profile.user_type != 'recruiter':
        messages.error(request, 'Only recruiters can post jobs')
        return redirect('dashboard')
    
    try:
        recruiter_profile = user_profile.recruiterprofile
    except RecruiterProfile.DoesNotExist:
        return redirect('profile_setup')
    
    if request.method == 'POST':
        form = JobPostForm(request.POST)
        if form.is_valid():
            job_post = form.save(commit=False)
            job_post.recruiter = recruiter_profile
            job_post.save()
            messages.success(request, 'Job posted successfully!')
            return redirect('dashboard')
    else:
        form = JobPostForm()
    
    return render(request, 'post_job.html', {'form': form})

@login_required
def job_detail_view(request, job_id):
    job = get_object_or_404(JobPost, id=job_id)
    
    if request.user.userprofile.user_type == 'jobseeker':
        try:
            job_seeker_profile = request.user.userprofile.jobseekerprofile
            applied = Application.objects.filter(job_post=job, job_seeker=job_seeker_profile).exists()
        except JobSeekerProfile.DoesNotExist:
            applied = False
    else:
        applied = False
    
    return render(request, 'job_detail.html', {'job': job, 'applied': applied})

@login_required
def apply_job_view(request, job_id):
    job = get_object_or_404(JobPost, id=job_id)
    
    if request.user.userprofile.user_type != 'jobseeker':
        messages.error(request, 'Only job seekers can apply for jobs')
        return redirect('job_detail', job_id=job_id)
    
    try:
        job_seeker_profile = request.user.userprofile.jobseekerprofile
    except JobSeekerProfile.DoesNotExist:
        messages.error(request, 'Please complete your profile first')
        return redirect('profile_setup')
    
    if Application.objects.filter(job_post=job, job_seeker=job_seeker_profile).exists():
        messages.error(request, 'You have already applied for this job')
        return redirect('job_detail', job_id=job_id)
    
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.job_post = job
            application.job_seeker = job_seeker_profile
            application.save()
            messages.success(request, 'Application submitted successfully!')
            return redirect('dashboard')
    else:
        form = ApplicationForm()
    
    return render(request, 'apply_job.html', {'form': form, 'job': job})

@login_required
def upload_resume_view(request):
    if request.user.userprofile.user_type != 'jobseeker':
        messages.error(request, 'Only job seekers can upload resumes')
        return redirect('dashboard')
    
    try:
        job_seeker_profile = request.user.userprofile.jobseekerprofile
    except JobSeekerProfile.DoesNotExist:
        messages.error(request, 'Please complete your profile first')
        return redirect('profile_setup')
    
    if request.method == 'POST':
        form = ResumeUploadForm(request.POST, request.FILES, instance=job_seeker_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Resume uploaded successfully!')
            return redirect('dashboard')
    else:
        form = ResumeUploadForm(instance=job_seeker_profile)
    
    return render(request, 'upload_resume.html', {'form': form})

@login_required
def applications_view(request):
    user_profile = request.user.userprofile
    
    if user_profile.user_type == 'recruiter':
        try:
            recruiter_profile = user_profile.recruiterprofile
            applications = Application.objects.filter(job_post__recruiter=recruiter_profile)
            return render(request, 'recruiter_applications.html', {'applications': applications})
        except RecruiterProfile.DoesNotExist:
            return redirect('profile_setup')
    else:
        try:
            job_seeker_profile = user_profile.jobseekerprofile
            applications = Application.objects.filter(job_seeker=job_seeker_profile)
            return render(request, 'job_seeker_applications.html', {'applications': applications})
        except JobSeekerProfile.DoesNotExist:
            return redirect('profile_setup')

@login_required
def update_application_status_view(request, application_id):
    if request.user.userprofile.user_type != 'recruiter':
        messages.error(request, 'Only recruiters can update application status')
        return redirect('dashboard')
    
    application = get_object_or_404(Application, id=application_id)
    
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in dict(Application.APPLICATION_STATUS):
            application.status = status
            application.save()
            messages.success(request, 'Application status updated successfully!')
        else:
            messages.error(request, 'Invalid status')
    
    return redirect('applications')