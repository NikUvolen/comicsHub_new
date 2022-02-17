from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib.auth.views import LogoutView

from .views import UserProfile, profile

urlpatterns = [
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('update-profile/', profile, name='update_profile'),
    path('<str:username>/', UserProfile.as_view(), name='user_profile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
