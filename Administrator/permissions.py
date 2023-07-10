from .models import User,UserRole,Role,ChartRole
from functools import wraps
from django.http import HttpResponseForbidden
from .models import UserRole

def permission_required(*permission):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            user_id = User.objects.get(username = request.user)
            print(UserRole.objects.filter(user=user_id, field_role__in=permission))
            if UserRole.objects.filter(user=user_id, field_role=permission).exists():
                # User has the required permission
                return view_func(request, *args, **kwargs)
            else:
                # User does not have the required permission
                return HttpResponseForbidden("You do not have permission to access this page.")
        return wrapper
    return decorator




