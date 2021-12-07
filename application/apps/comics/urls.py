from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views
from .models import Comics, LikesDislikes
from .views import ComicsViewPage, DetailComicsView, add_comics, DeleteComics, AllComicsView, AuthorsComicsView

urlpatterns = [
    path('', ComicsViewPage.as_view(), name='home'),
    path('comics/<str:slug>', DetailComicsView.as_view(), name='detail_comics_view'),
    path('add-comics/', add_comics, name='add-comics'),
    path('comics/', AllComicsView.as_view(), name='all-comics'),
    path('comics/authors_comics/<str:username>', AuthorsComicsView.as_view(), name='authors-comics'),

    url('delete-comics/<str:slug>/', DeleteComics.as_view(), name='delete_comics'),
    url(r'^comics/comics/(?P<pk>\d+)/like/$',
        login_required(views.VoteView.as_view(model=Comics, vote_type=LikesDislikes.LIKE)),
        name='comics_like'),
    url(r'^comics/comics/(?P<pk>\d+)/dislike/$',
        login_required(views.VoteView.as_view(model=Comics, vote_type=LikesDislikes.DISLIKE)),
        name='comics_dislike'),
]
