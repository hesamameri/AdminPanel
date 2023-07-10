from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from Administrator.models import User,UserRole

@login_required(login_url='Administrator:login_view')
def index(request):
    user_id = User.objects.get(username = request.user)
    user_permissions = UserRole.objects.filter(user = user_id).values('field_role')
    user_permissions = [item['field_role'] for item in user_permissions]
    context = {
        'user_permissions': user_permissions,
    }
    return render(request,'./Home/index.html',context=context)
