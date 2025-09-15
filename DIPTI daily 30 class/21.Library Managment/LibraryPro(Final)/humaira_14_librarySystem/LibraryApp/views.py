from django.shortcuts import render, redirect


from django.contrib.auth import authenticate, login, logout
from LibraryApp.models import *
from django.contrib.auth.decorators import login_required 

@login_required(login_url='logIn')
def studentDashboard(req):
    
    return render(req, 'studentDashboard.html')

@login_required(login_url='logIn')
def librarianDashboard(req):
    return render(req, 'librarianDashboard.html')

@login_required(login_url='logIn')
def studentProfile(req):
    return render(req, 'studentProfile.html')

@login_required(login_url='logIn')
def librarianProfile(req):
    data = librarianProfileModel.objects.get(user=req.user)
    context = {
        'data' : data
    }
    return render(req, 'librarianProfile.html', context)

def signUp(req):
    if req.method=='POST':
        username = req.POST.get('username')
        email = req.POST.get('email')
        userTypes = req.POST.get('userTypes')
        password = req.POST.get('password')
        confirm_password = req.POST.get('confirm_password')

        
        if password == confirm_password:
            user = customUserModel.objects.create_user(
                username = username,
                email = email,
                password = password,
                userTypes = userTypes, 
            )
            if userTypes == 'Librarian':
                userLib = librarianProfileModel.objects.create(
                user=user
                )
                userLib.save()       
            else:
                userLib = studentProfileModel.objects.create(user=user)
                userLib.save()
            return redirect('logIn')
    return render(req, 'signUp.html')

def logIn(req):
    if req.method=='POST':
        Username = req.POST.get('username')
        Password = req.POST.get('password')
        customuser=customUserModel.objects.get(username=Username)
        
        user = authenticate(req, username=Username, password=Password)
        
        if user is not None:
            login(req, user)
            if customuser.userTypes == 'Librarian':
                
                return redirect('librarianDashboard')
            
            else:
                
                return redirect('studentDashboard')     
                     
    return render(req, 'logIn.html')

@login_required(login_url='logIn')
def logOut(req):
    logout(req)
    return redirect('logIn')

@login_required(login_url='logIn')
def changePassword(req):
    if req.method=='POST':
        oldPassword = req.POST.get('oldPassword')
        newPassword = req.POST.get('newPassword')
        confirmPassword = req.POST.get('confirmPassword')
        if newPassword == confirmPassword:
            if req.user.check_password(oldPassword):
                req.user.set_password(newPassword)
                req.user.save()
                logout(req)
                return redirect('logIn')
    return render(req, 'changePassword.html')
@login_required(login_url='logIn')
def addBook(req):
    if req.method=='POST':
        title = req.POST.get('title')
        author = req.POST.get('author')
        isbn = req.POST.get('isbn')
        quantity = req.POST.get('quantity')

        userLib = librarianProfileModel.objects.get(user=req.user)

        data = bookModel(
            librarianProfileModel=userLib,
            title=title,
            author=author,
            isbn=isbn,
            quantity=quantity,      
        )
        data.save()
        return redirect ('listBok')
    return render(req,"addBook.html")
@login_required(login_url='logIn')
def listBok(req):
    data=bookModel.objects.all()
    context={
        'data':data          
    }
    return render(req,"listBok.html",context)

@login_required(login_url='logIn')
def deleteBook(req, id):
    data = bookModel.objects.get(id=id).delete()
    return redirect ('listBok')

@login_required(login_url='logIn')
def editBook(req,id):
    data=bookModel.objects.get(id=id)
    context={
        'data':data
    }
    if req.method=='POST':
        data.id=id
        data.title=req.POST.get('title')
        data.author=req.POST.get('author')
        data.isbn=req.POST.get('isbn')
        data.quantity=req.POST.get('quantity')
        data.save()
        return redirect ('listBok')

    return render(req,"editBook.html",context)

def editLibrianProfile(req):
    if req.method == 'POST':
        employee_id = req.POST.get('employee_id')
        designation = req.POST.get('designation')
        contact_number = req.POST.get('contact_number')
        address = req.POST.get('address')
        if req.FILES.get('profile_picture'):
            profile_picture = req.FILES.get('profile_picture')
        profile_picture = req.FILES.get('profile_picture')

        data = librarianProfileModel(
            user = req.user,
            employee_id = employee_id,
            designation = designation,
            contact_number = contact_number,
            address = address,
            profile_picture = profile_picture
        )
        data.save()
        return redirect('librarianProfile')
    return render(req, 'editLibrianProfile.html')

def editStudentProfile(req):
    if req.method == 'POST':
        student_id = req.POST.get('student_id')
        department = req.POST.get('department')
        phone = req.POST.get('phone')
        address = req.POST.get('address')
        if req.FILES.get('profile_picture'):
            profile_picture = req.FILES.get('profile_picture')
        profile_picture = req.FILES.get('profile_picture')

        data = librarianProfileModel(
            user = req.user,
            student_id = student_id,
            department = department,
            phone = phone,
            address = address,
            profile_picture = profile_picture
        )
        data.save()
        return redirect('studentProfile')
    return render(req, 'editStudentProfile.html')