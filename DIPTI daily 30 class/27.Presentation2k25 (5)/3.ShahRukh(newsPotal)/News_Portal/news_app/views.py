from django.shortcuts import render,redirect,get_object_or_404
from news_app.models import *
from news_app.forms import *
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required, user_passes_test


from django.contrib.auth.decorators import login_required



def dashboard(request):
    news_queryset = NewsModel.objects.all().order_by('-published_date')
    paginator = Paginator(news_queryset, 10)  # 10 news per page
    page_number = request.GET.get('page')
    news_page = paginator.get_page(page_number)

    context = {
        'news_list': news_page
    }
    return render (request, "news_app/admin_dashboard.html",context)

def news_list_views (request):
    news_queryset = NewsModel.objects.all().order_by('-published_date')
    paginator = Paginator(news_queryset, 10)  # 10 news per page
    page_number = request.GET.get('page')
    news_page = paginator.get_page(page_number)

    context = {
        'news_list': news_page
    }
    return render(request, 'news/news.html', context)


def add_news_views(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            news = form.save(commit=False)
            news.save()
            messages.success(request, 'News added successfully!')
            return redirect('news')  
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = NewsForm()
    
    context = {
        'form': form
    }
    return render(request, 'news/add_news.html', context)

def edit_news(request, id):
    news = get_object_or_404(NewsModel, id=id)

   
  

    if request.method == "POST":
        form = NewsForm(request.POST, request.FILES, instance=news)
        if form.is_valid():
            form.save()
            return redirect("news")  # list এ ফেরত যাবে
    else:
        form = NewsForm(instance=news)

    return render(request, "news/edit_news.html", {"form": form, "news": news})


def delete_news(request, id):
    news = get_object_or_404(NewsModel, id=id)
    news.delete()
    return redirect("news") 


def is_admin(user):
    return user.is_authenticated and user.role == "Admin"

@login_required
@user_passes_test(is_admin)
def approve_news(request, id):
    news = get_object_or_404(NewsModel, id=id)
    news.status = "Published"
    news.save()
    return redirect('news') 


@login_required
@user_passes_test(is_admin)
def reject_news(request, id):
    news = get_object_or_404(NewsModel, id=id)
    news.status = "Rejected"
    news.save()
    return redirect('news')


def authors_views(request):
    authors = CustomUserModel.objects.filter(role='Author')
    return render(request, "news_app/authors.html", {"authors": authors})


def add_author_views(request):
    if request.method == "POST":
        username = request.POST.get("username")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        profile = request.FILES.get("profile")

        # check username exists or not
        if CustomUserModel.objects.filter(username=username).exists():
            messages.error(request, "❌ username is unvalid")
            return redirect("add_author") 


        CustomUserModel.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            profile=profile
            
        )
        messages.success(request, "✅ Author succesfull regestation")
        return redirect("authors")
    return render(request, "news_app/add_author.html")

# Edit Author
def edit_author_views(request, pk):
   author = get_object_or_404(CustomUserModel, id=pk)

   if request.method == "POST":
        author.username = request.POST.get("username")
        author.first_name = request.POST.get("first_name")
        author.last_name = request.POST.get("last_name")
        author.email = request.POST.get("email")
        author.phone = request.POST.get("phone")

        if request.FILES.get("profile"):  
            author.profile = request.FILES.get("profile")

        # username unique কিনা সেটা check করা দরকার
        if CustomUserModel.objects.filter(username=author.username).exclude(id=author.id).exists():
            messages.error(request, "❌ username is Unvalid")
            return redirect("edit_author", author_id=author.id)

        author.save()
        messages.success(request, "✅ Author Succesfully Update")
        return redirect("authors") 

   return render(request, "news_app/edit_author.html", {"author": author})

def author_delete(request,d):
    author = get_object_or_404(CustomUserModel, id=d)
    author.delete()
    return redirect("authors") 


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            messages.success(request, "✅ Logged in successfully")
            return redirect("dashboard")  
        else:
            messages.error(request, "❌ Invalid username or password")

    return render(request, "news_app/login.html")

def logout_view(request):
    logout(request)
    return redirect("login_view")


def category_list_views(request):
    categories = CategoryModel.objects.all()
    return render(request, 'catagories/catagories_list.html', {'categories': categories})

def add_category_views(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)  
        if form.is_valid():
            form.save()
            return redirect('category_list')  
    else:
        form = CategoryForm()
    return render(request, 'catagories/add_category.html', {'form': form})
def delete_category(request, id):
    category = get_object_or_404(CategoryModel, id=id)
    category.delete()
    return redirect('category_list')




def update_category(request, id):
    category = get_object_or_404(CategoryModel, id=id)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')  # update শেষে list এ যাবে
    else:
        form = CategoryForm(instance=category)  # পুরানো ডাটা দেখাবে
    return render(request, "catagories/update_category.html", {"form": form})


