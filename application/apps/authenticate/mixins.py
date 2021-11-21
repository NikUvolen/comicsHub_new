from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect


class AnonymityRequiredMixin(AccessMixin):
    login_url = 'home'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)
