from django.shortcuts import render , redirect
from .models import jobApplicationModel , CandidateProfileModel
from employer_app.models import jobModel 

def application_list(request):
    if hasattr(request.user, 'candidate_profile'):
        candidate_profile = request.user.candidate_profile
        applications = jobApplicationModel.objects.filter(candidate=candidate_profile).select_related('job')
        heading = "My Applications"
    

    elif hasattr(request.user, 'employer_profile'):
        employer_profile = request.user.employer_profile
        applications = jobApplicationModel.objects.filter(job__employer=employer_profile).select_related('candidate', 'job')
        heading = "Candidates Who Applied to My Jobs"
    return render(request, 'appliedjoblist.html', {
        'applications': applications,
        'heading': heading
    })

def add_applied_job(request):
    if request.method == 'POST':
        job_id = request.POST.get('job_id')
        job = jobModel.objects.get(id=job_id)
        candidate_profile = CandidateProfileModel.objects.get(candidate_user=request.user)


        if not jobApplicationModel.objects.filter(job=job, candidate=candidate_profile).exists():
            last_education = request.POST.get('last_education')
            work_experience = request.POST.get('work_experience')

            jobApplicationModel.objects.create(
                job=job,
                candidate=candidate_profile,
                last_education=last_education,
                work_experience=work_experience,
                status='applied'
            )
            return redirect('application_list') 

    return redirect('home')

