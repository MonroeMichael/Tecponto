from .models import total_points

def points(request):
    if request.user.is_authenticated:
        return {'player_points': total_points(request.user)}
    return {}
