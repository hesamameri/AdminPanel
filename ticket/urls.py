from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name = 'ticket'
urlpatterns = [
    path('indexticket', views.index_ticket_view, name='indexTicket'),
    path('confirmticket', views.confirm_ticket_view, name='confirmTicket'),
    path('inboxticket', views.inbox_ticket_view, name='inboxTicket'),
    path('newticket', views.new_ticket_view, name='newTicket'),
    path('organticket', views.organ_ticket_view, name='organTicket'),
    path('qualityticket', views.quality_ticket_view, name='qualityTicket'),
    path('sentticket', views.sent_ticket_view, name='sentTicket'),
    path('viewticket/<int:arg>/', views.view_ticket_view, name='viewTicket'),
    # path('viewticket/update/<int:ticket_id>/<int:item_id>', views.change_view_item, name='viewTicketUpdate'),
    path('viewticketQuality', views.viewQuality_ticket_view, name='viewTicketQuality'),
    
   
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)