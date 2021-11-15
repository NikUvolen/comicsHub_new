from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import test_page

urlpatterns = [
    path('', test_page)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
