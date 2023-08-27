from Administrator.models import User
from Administrator.models import User,UserRole,UserChart
from ticket.models import Ticket,TicketSystemCategory
def user_data(request):

    user_permissions = []
    ticketsystem_categories = []
    if request.user.is_authenticated:
        user_id = User.objects.get(username = request.user)
        user_permissions = UserRole.objects.filter(user = user_id).values('field_role')
        user_permissions = [item['field_role'] for item in user_permissions]
        user_chart = UserChart.objects.filter(user_id=user_id)
        user_chart_ids = [obj.chart.chart_id for obj in user_chart]
        ticketsystem_categories = TicketSystemCategory.objects.filter(chart_id__in=user_chart_ids)
    context = {
        'ticketsystem_categories':ticketsystem_categories,
        'user_permissions': user_permissions,
    }
    return context