from django.contrib import admin
from django.urls import path, include
from news_app.views import *
from django.conf import settings
from django.conf.urls.static import static
from youngsouthasian_app.views import *



urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    
    path("d/",dashboard, name="dashboard"),
    path("news/",news_list_views, name="news"),
    path("add_news/",add_news_views,name="add_news"),
    path("edit_news/<int:id>/",edit_news,name="edit_news"),
    path("delete_news/<int:id>/",delete_news,name="delete_news"),
    path("delete_news/<int:id>/",reject_news,name="reject_news"),
    path("delete_news/<int:id>/",approve_news,name="approve_news"),
    
    path("authors/",authors_views,name="authors"),
    path("add_author/",add_author_views,name="add_author"),
    path("login/",login_view,name="login_view"),
    path("logout/",logout_view,name="logout_view"),
    path("edit_author/<str:pk>/",edit_author_views,name="edit_author"),
    path("author_delete/<int:d>/", author_delete, name="author_delete"),

    
    path('category_list_views/', category_list_views, name='category_list'),
    path('add-category/', add_category_views, name='add_category'),
    path('d-category/<int:id>/', delete_category, name='delete_category'),
    path('u-category/<int:id>/', update_category, name='update_category'),
    
    
    path("privacy_policy/", privacy_policy, name="privacy_policy"),
    path("news_detail/<int:id>", news_detail, name="news_detail"),
    
    
    #Catagory wise news show
    path('', index_view, name='category_news'),
    path('category/<slug:category_slug>/', category_news, name='category_news'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

