from django.shortcuts import render
from news_app.models import NewsModel, CategoryModel
from django.shortcuts import get_object_or_404

def privacy_policy(request):
    return render(request, "privacy_policy.html")

def index_view(request):
    # Fetch top 5 news, ordered by published date
    top_news = NewsModel.objects.all().order_by('-published_date')[:5]
    
    # Divide the top news into left and right news
    left_news = top_news[:1]
    right_news = top_news[1:]
    
    # Fetch categories safely, with error handling in case a category is missing
    try:
        sports_category = CategoryModel.objects.get(catagory_name='Sports')
        tech_category = CategoryModel.objects.get(catagory_name='Technology')
        business_category = CategoryModel.objects.get(catagory_name='Business')
        entertainment_category = CategoryModel.objects.get(catagory_name='Entertainment')
        international_category = CategoryModel.objects.get(catagory_name='International')
        lifestyle_category = CategoryModel.objects.get(catagory_name='Lifestyle')
    except CategoryModel.DoesNotExist:
        # Handle missing category gracefully, you might want to log or set defaults
        sports_category = tech_category = business_category = entertainment_category = international_category = lifestyle_category = None

    # Fetch news for each category, ensuring it’s only "Published" news
    sports_news = NewsModel.objects.filter(category=sports_category, status='Published').order_by('-published_date')[:6] if sports_category else []
    tech_news = NewsModel.objects.filter(category=tech_category, status='Published').order_by('-published_date')[:6] if tech_category else []
    business_news = NewsModel.objects.filter(category=business_category, status='Published').order_by('-published_date')[:6] if business_category else []
    entertainment_news = NewsModel.objects.filter(category=entertainment_category, status='Published').order_by('-published_date')[:6] if entertainment_category else []
    international_news = NewsModel.objects.filter(category=international_category, status='Published').order_by('-published_date')[:6] if international_category else []
    lifestyle_news = NewsModel.objects.filter(category=lifestyle_category, status='Published').order_by('-published_date')[:6] if lifestyle_category else []

    # Get the first news for "International" and "Lifestyle" categories, if available
    first_news = international_news.first()  
    other_news = international_news[1:6] 

    first_life_news = lifestyle_news.first()  
    other_life_news = lifestyle_news[1:6]
    
    # Context to pass to the template
    context = {
        'top_news': top_news,
        'left_news': left_news, 
        'right_news': right_news,
        'sports_news': sports_news,
        'tech_news': tech_news,
        'business_news': business_news,
        'entertainment_news': entertainment_news,
        'international_news': international_news,
        'first_news': first_news,
        'other_news': other_news,
        'lifestyle_news': lifestyle_news,
        'first_life_news': first_life_news,
        'other_life_news': other_life_news,
    }

    return render(request, 'index.html', context)

def news_detail(request, id):
    news_item = get_object_or_404(NewsModel, id=id)
    recent_news = NewsModel.objects.exclude(id=id).order_by('-published_date')[:5]

    return render(request, 'news_details.html', {
        'news_item': news_item,
        'recent_news': recent_news
    })

def category_news(request, category_slug):
    category = get_object_or_404(CategoryModel, slug=category_slug)
    news_list = NewsModel.objects.filter(category=category).order_by('-published_date')

    recent_news = NewsModel.objects.all().order_by('-published_date')[:5]  
    context = {
        'category': category,
        'news_list': news_list,
        'recent_news': recent_news,
    }
    return render(request, 'section_news.html', context)