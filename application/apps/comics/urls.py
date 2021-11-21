from django.urls import path

from .views import ComicsViewPage

urlpatterns = [
    path('', ComicsViewPage.as_view(), name='home')
]
