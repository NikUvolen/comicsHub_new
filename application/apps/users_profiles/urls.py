from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib.auth.views import LogoutView

from .views import test_page

urlpatterns = [
    path('', test_page),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
