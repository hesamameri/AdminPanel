from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name = 'ticket'
urlpatterns = [
    path('indexticket', views.index_ticket_view, name='indexTicket'),
    path('indexticket/<int:user_id>/<str:status_name>/', views.index_admin_ticket_view, name='indexAdminTicket'),
    path('confirmticket', views.confirm_ticket_view, name='confirmTicket'),
    path('inboxticket', views.inbox_ticket_view, name='inboxTicket'),
    path('newticket', views.new_ticket_view, name='newTicket'),
    path('organticket/<int:organ_id>', views.organ_ticket_view, name='organTicket'),
    path('qualityticket', views.quality_ticket_view, name='qualityTicket'),
    path('sentticket', views.sent_ticket_view, name='sentTicket'),
    path('viewticket/<int:arg>/', views.view_ticket_view, name='viewTicket'),
    path('qualityticket/<int:ticket_id>', views.viewQuality_ticket_view, name='viewTicketQuality'),
    
   
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)