from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name = 'home'
urlpatterns = [
    path('home/', views.index, name='index'),
   

   
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)