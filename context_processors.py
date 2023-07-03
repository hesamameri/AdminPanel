
def common_data(request):
    pass
from Administrator.models import User

def user_data(request):

    user = request.session['user_id']
    user = User.objects.filter(user_id = user)[0]
    
    context = {
        'user': user,
    }
    return context