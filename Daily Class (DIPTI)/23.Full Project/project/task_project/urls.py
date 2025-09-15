from django.contrib import admin
from django.urls import path
from task_app.views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', loginpage , name='loginpage'),
    path('registerpage/', registerpage , name='registerpage'),
    path('changepasswordpage', changepasswordpage, name='changepasswordpage'),
    path('logoutpage/', logoutpage, name='logoutpage'),
    
    
    
    path('homepage/', homepage , name='homepage'),
    path('taskpage/', taskpage , name='taskpage'),
    path('createtask/', createtask , name='createtask'),
    path('cardtask/', cardtask , name='cardtask'),
    path('task_view/<str:id>', task_view , name='task_view'),
    path('task_edit/<str:id>', task_edit, name='task_edit'),
    path('task_delete/<str:id>', task_delete, name='task_delete'),
    
    
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
