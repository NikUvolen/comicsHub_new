from django.urls import path

from .views import test_page

urlpatterns = [
    path('', test_page)
]