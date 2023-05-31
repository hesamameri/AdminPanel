from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.login_view, name='login'),
    path('post/', views.login_post, name='login_post'),
    path('otp/', views.otp, name='otp'),
    # path('otp/post', views.otp_post, name='otp_post'),

   
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
