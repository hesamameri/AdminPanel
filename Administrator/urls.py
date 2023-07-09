from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView
app_name = 'Administrator'

urlpatterns = [
    path('', views.login_view, name='login_view'),
    # path('logout/<int:user_id>', views.logout, name='logout'),
    path('otp/', views.otp, name='otp'),
    path('logout/', views.logout_view, name='logout_view'),

   
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
