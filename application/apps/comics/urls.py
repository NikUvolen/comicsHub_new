from django.urls import path

from .views import (MainPage, DetailViewComics, UserComics,
                    AddComics, delete_comment)


urlpatterns = [
    path('', MainPage.as_view(), name='main_page'),
    path('comics/<str:comics_slug>/', DetailViewComics.as_view(), name='view_comics'),
    path('add-comics/', AddComics.as_view(), name='add_comics'),

    path('ajax/user_comics/<int:pk>', UserComics.as_view(), name='user_comics'),
    path('ajax/delete-comment/<int:pk>', delete_comment, name='delete-comment')
    # path('ajax/add-comment/<str:comics_slug>', add_comment, name='add-comment-ajax')
]