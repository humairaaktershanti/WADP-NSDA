from django.shortcuts import render, redirect
from ECommerceApp.models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

from django.contrib.auth.hashers import check_password

messagesBox = {
    'success_msg': 'Successfully Created',
    'password_msg': 'Password and Confirm Password not matched',
    'username_msg': 'Username and Password not matched',
    'userexist_msg': 'Username already existed.',
    'delete_msg': 'Delete Successfully',
    'update_msg': 'Update Successfully',
    'passerror_msg': 'Passowrod Not Valid',
}

def signupPage(request):
    if request.method == 'POST':
        fullname=request.POST.get('fullname')
        username=request.POST.get('username')
        usertype=request.POST.get('usertype')
        gender=request.POST.get('gender')
        profileimg=request.FILES.get('profileimg')
        pass_word=request.POST.get('pass_word')
        confirmpassword=request.POST.get('confirmpassword')
        
        if pass_word == confirmpassword:
            user = ECommerceUser.objects.create_user(username=username, password=pass_word)
            user.FullName = fullname
            user.UserType = usertype
            user.Gender = gender
            user.ProfileImg = profileimg
            

            if user.UserType == 'Customer':
                CustomerInfoModel.objects.create(EUser = user)
                ContactInfoModel.objects.create(EUser = user)
                
            elif user.UserType == 'Seller':
                SellerInfoModel.objects.create(EUser = user)
                ContactInfoModel.objects.create(EUser = user)
            
            
            user.save()
            messages.success(request,messagesBox['success_msg'])
            return redirect('signinPage')
        else:
            messages.error(request,messagesBox['password_msg'])

    return render(request,'signuppage.html')

def signinPage(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        
        myuser = authenticate(username=username, password=password)
        
        if myuser:
            login(request,myuser)
            return redirect('dashboard')
        else:
            messages.error(request,messagesBox['username_msg'])
    
    return render(request,'signinpage.html')

@login_required
def dashboard(request):
    
    return render(request,'dashboard.html')

def logoutPage(request):
    
    logout(request)
    
    return redirect('signinPage')

@login_required
def addProductPage(request):
    
    if request.method == 'POST':
        ProductName = request.POST.get('ProductName')
        ProductCategory = request.POST.get('ProductCategory')
        ProductDescription = request.POST.get('ProductDescription')
        ProCompanyName = request.POST.get('ProCompanyName')
        ProCompanyAddress = request.POST.get('ProCompanyAddress')
        ProductPrice = request.POST.get('ProductPrice')
        
        current_user = request.user
        
        addproduct = ProductModel(
            ProductName=ProductName,
            ProductCategory=ProductCategory,
            ProductDescription=ProductDescription,
            ProCompanyName=ProCompanyName,
            ProCompanyAddress=ProCompanyAddress,
            ProductPrice=ProductPrice,
            Added_by=current_user,
        )
        addproduct.save()
        return redirect('productlistPage')
        
    return render(request,'Seller/addProduct.html')

@login_required
def productlistPage(request):
    current_userType = request.user.UserType
    current_user = request.user
    
    if current_userType == 'Seller':
        productinfo = ProductModel.objects.filter(Added_by = current_user)
    else:       
        productinfo = ProductModel.objects.all()
    
    prodictdict = {
        'productinfo':productinfo
    }
    
    return render(request,'productlist.html',prodictdict)

def deleteproduct(request,proid):
    
    productinfo = ProductModel.objects.get(id = proid)
    productinfo.delete()
    
    
    messages.success(request, messagesBox['delete_msg'])
    return redirect('productlistPage')

@login_required
def viewProductPage(request, proid):
    productinfo = ProductModel.objects.get(id = proid)
    prodictdict = {
        'productinfo':productinfo
    }
    
    return render(request,'viewproduct.html',prodictdict)

@login_required
def editProduct(request, proid):
    productinfo = ProductModel.objects.get(id = proid)
    prodictdict = {
        'productinfo':productinfo
    }
    return render(request,'Seller/editproduct.html',prodictdict)

def updateProduct(request):
    if request.method == 'POST':
        ProductId = request.POST.get('ProductId')
        ProductName = request.POST.get('ProductName')
        ProductCategory = request.POST.get('ProductCategory')
        ProductDescription = request.POST.get('ProductDescription')
        ProCompanyName = request.POST.get('ProCompanyName')
        ProCompanyAddress = request.POST.get('ProCompanyAddress')
        ProductPrice = request.POST.get('ProductPrice')
        
        current_user = request.user
        
        updateProductdata = ProductModel(
            id = ProductId,
            ProductName=ProductName,
            ProductCategory=ProductCategory,
            ProductDescription=ProductDescription,
            ProCompanyName=ProCompanyName,
            ProCompanyAddress=ProCompanyAddress,
            ProductPrice=ProductPrice,
            Added_by=current_user,
        )
        updateProductdata.save()
        messages.success(request,messagesBox['update_msg'])
        return redirect('productlistPage')

@login_required
def profilePage(request):
    
    return render(request,'Profile/profile.html')


@login_required
def basicinfoPage(request):
    
    return render(request,'Profile/basicinfo.html')
@login_required
def contactinfoPage(request):
    
    return render(request,'Profile/contactinfo.html')

@login_required
def editprofilePage(request):
    current_user = request.user
    current_userType = request.user.UserType
    if request.method == 'POST':
        fullname=request.POST.get('fullname')
        gender=request.POST.get('gender')
        address=request.POST.get('address')
        mobile=request.POST.get('mobile')
        email=request.POST.get('email')
        fbid=request.POST.get('fbid')
        companyname=request.POST.get('companyname')
        comapnyaddress=request.POST.get('comapnyaddress')
        sellingexp=request.POST.get('sellingexp')
        intsproduct=request.POST.get('intsproduct')
        referenceid=request.POST.get('referenceid')
        
        profileimg=request.FILES.get('profileimg')
        pass_word=request.POST.get('pass_word')
        confirmpassword=request.POST.get('confirmpassword')
        
        if pass_word == confirmpassword:
            if check_password(pass_word,current_user.password):
                current_user.FullName = fullname
                current_user.Gender = gender
                current_user.email = email
                current_user.ProfileImg = profileimg
                
                if current_userType == 'Seller':
                    seller_user = current_user.sellerinfomodel
                    
                    seller_user.CompanyName = companyname
                    seller_user.CompanyAddress = comapnyaddress
                    seller_user.SellingExperience = sellingexp
                    seller_user.save()
                    
                else:
                    customer_user = current_user.customerinfomodel
                    
                    customer_user.InterestedProduct = intsproduct
                    customer_user.ReferenceID = referenceid
                    customer_user.save()
                    
                contact_user = current_user.contactinfomodel
                contact_user.Mobile = mobile
                contact_user.Address = address
                contact_user.FacebookID =fbid
                
                current_user.save()
                contact_user.save()
                messages.success(request,messagesBox['update_msg'])           
                return redirect('profilePage')
                
            else:
                messages.error(request,messagesBox['passerror_msg'])
        else:
            messages.error(request,messagesBox['password_msg'])
            
    
    return render(request,'Profile/editprofile.html')