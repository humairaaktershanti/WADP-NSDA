from django.shortcuts import render, redirect
from task_app.models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password

#function of registerpage
def registerpage(req):
    if req.method=='POST':
        username=req.POST.get('username')
        firstname=req.POST.get('firstname')
        email=req.POST.get('email')
        profile_photo=req.FILES.get('profile_photo')
        bio=req.POST.get('bio')
        password=req.POST.get('password')
        confirm_password=req.POST.get('confirm_password')
        
        if password== confirm_password:
            customuserModel.objects.create_user(
                username=username,
                first_name=firstname,
                email=email,
                profile_photo=profile_photo,
                bio=bio,
                password=confirm_password,
            )
            return redirect('loginpage')
            
    return render(req, "registerpage.html")

#function of loginpage

def loginpage(req):
    if req.method== 'POST':
        username=req.POST.get('username')
        password=req.POST.get('password')
        
        user=authenticate(req, username=username, password=password)
        if user:
            login(req, user)
            return redirect('homepage')
    return render(req, 'loginpage.html')

#Function of Changepasswordpage
@login_required
def changepasswordpage(req):
    
    current_user=req.user
    if req.method == 'POST':
        current_password=req.POST.get('current_password')
        new_password=req.POST.get('new_password')
        confirm_password=req.POST.get('confirm_password')
        
        if check_password(current_password, req.user.password):
            if new_password==confirm_password:
                current_user.set_password(new_password)
                current_user.save()
                return redirect('homepage')
    
    return render(req, 'changepasswordpage.html')

#Function of Homepage
@login_required
def homepage(req):
    
    return render(req, 'homepage.html')

#Function of logoutpage
@login_required
def logoutpage(req):
    logout(req)
    return redirect('loginpage')

#Function of taskpage
@login_required
def taskpage(req):
    
    info=taskModel.objects.filter(user=req.user)
    context={
        'task':info
    }
    return render(req, 'taskpage.html', context)


#function of createtask
@login_required
def createtask(req):
    
    if req.method=='POST':
        title=req.POST.get('title')
        description=req.POST.get('description')
        due_date=req.POST.get('due_date')
        priority=req.POST.get('priority')
        status=req.POST.get('status')

        task=taskModel(
            user=req.user,
            title=title,
            description=description,
            due_date=due_date,
            priority=priority,
            status=status,
        )
        task.save()  
        return redirect('taskpage')
            
    return render(req, "createtask.html")


# #function of extra_task_add
# @login_required
# def extra_task_add(req):
    
#     if req.method=='POST':
#         title=req.POST.get('title')
#         description=req.POST.get('description')
#         due_date=req.POST.get('due_date')
#         priority=req.POST.get('priority')
#         status=req.POST.get('status')

#         task=taskModel(
#             user=req.user,
#             title=title,
#             description=description,
#             due_date=due_date,
#             priority=priority,
#             status=status,
#         )
#         task.save()  
#         return redirect('taskpage')
            
#     return render(req, "extra_task_add.html")
        

#Function of task_view
@login_required
def task_view(req, id):
    
    info=taskModel.objects.get(id=id)
    context={
        'task':info
    }
    return render(req, 'task_view.html', context)

#function of task_edit
@login_required
def task_edit(req, id):
    
    info=taskModel.objects.get(id=id)
    context={
        'task':info
    }
    
    if req.method=='POST':
        title=req.POST.get('title')
        description=req.POST.get('description')
        due_date=req.POST.get('due_date')
        priority=req.POST.get('priority')
        status=req.POST.get('status')

        task=taskModel(
            id=id,
            user=req.user,
            title=title,
            description=description,
            due_date=due_date,
            priority=priority,
            status=status,
        )
        task.save()  
        return redirect('taskpage')
            
    return render(req, "task_edit.html", context)

#Function of task_delete
@login_required
def task_delete(req, id):
    
    task=taskModel.objects.get(id=id)
    task.delete()
    return redirect('taskpage')

#Function of cardtask
@login_required
def cardtask(req):
    data=taskModel.objects.filter(user=req.user)
    Pending_task=taskModel.objects.filter(user=req.user, status='Pending')
    In_progress_task=taskModel.objects.filter(user=req.user, status='In progress')
    Completed_task=taskModel.objects.filter(user=req.user, status='Completed')
    
    context={
        'data':data,
        'Pending_task':Pending_task,
        'In_progress_task':In_progress_task,
        'Completed_task':Completed_task,
    }
    

    return render(req, 'cardtask.html', context)



