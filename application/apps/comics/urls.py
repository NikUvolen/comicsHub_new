from django.urls import path

from .views import ComicsViewPage, DetailComicsView

urlpatterns = [
    path('', ComicsViewPage.as_view(), name='home'),
    path('comics/<str:slug>', DetailComicsView.as_view(), name='detail_comics_view')
]
