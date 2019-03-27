from .models import Host

def host(request):
    return {
        'host': Host.objects.filter(user=request.user)
    }
