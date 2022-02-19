from django.urls import path

from .views import MainPage, DetailViewComics, UserComics, AddComics


urlpatterns = [
    path('', MainPage.as_view(), name='main_page'),
    path('comics/<str:comics_slug>/', DetailViewComics.as_view(), name='view_comics'),
    path('add-comics/', AddComics.as_view(), name='add_comics'),

    path('ajax/user_comics/<int:pk>', UserComics.as_view(), name='user_comics')
]