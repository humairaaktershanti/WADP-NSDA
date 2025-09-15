from django.shortcuts import render ,redirect
from .models import jobModel ,EmployerProfileModel



def job_list(request):
    employer_profile = EmployerProfileModel.objects.get(employer_user=request.user)
    jobs = jobModel.objects.filter(employer=employer_profile)
    return render(request, 'joblist.html', {'jobs': jobs})
def add_job(request):
    employer_profile = request.user.employer_profile 
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        requirements = request.POST.get('requirements')
        salary = request.POST.get('salary')
        job_type = request.POST.get('job_type')
        deadline = request.POST.get('deadline')

        jobModel.objects.create(
            employer=employer_profile,
            title=title,
            description=description,
            requirements=requirements,
            salary=salary,
            job_type=job_type,
            deadline=deadline
        )

        return redirect('job_list')
    return render(request, 'add_job.html')
def delete_job(request, id):
    jobModel.objects.get(id=id).delete()
    return redirect('job_list')
def edit_job(request, id):
    job = jobModel.objects.get(id=id)
    if request.method == 'POST':
        job.title = request.POST.get('title')
        job.description = request.POST.get('description')
        job.requirements = request.POST.get('requirements')
        job.salary = request.POST.get('salary')
        job.job_type = request.POST.get('job_type')
        job.deadline = request.POST.get('deadline')
        job.save()
        return redirect('job_list')
    return render(request, 'edit_job.html', {'job': job})
def view_job(request, id):
    job = jobModel.objects.get(id=id)
    return render(request, 'view_job.html', {'job': job})


