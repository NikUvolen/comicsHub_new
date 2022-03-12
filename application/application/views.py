from django.http import HttpResponse
from django.utils import timezone


def update_status(request):
    if request.user.is_authenticated:
        user = request.user
        user.last_login = timezone.now()
        user.save()
        return HttpResponse(200)
    return HttpResponse(200)
