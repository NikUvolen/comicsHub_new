from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required

from .views import UserRegistration, UserLogin, UserProfile, EditProfile


urlpatterns = [
    path('register/', UserRegistration.as_view(), name='user_registration'),
    path('auth/', UserLogin.as_view(), name='user_authentication'),
    path('logout/', login_required(LogoutView.as_view(next_page='/')), name='logout'),
    path('<int:pk>/', UserProfile.as_view(), name='user_profile'),
    path('edit-profile/', login_required(EditProfile.as_view()), name='edit_profile')
    # path('<str:username>/', UserProfile.as_view(), name='user_profile')
]
