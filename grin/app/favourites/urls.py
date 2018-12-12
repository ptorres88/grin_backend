# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from django.urls import path
from app.favourites.views import (FavouritesListView,
	FavouritePlaceSerializer,
	FavouriteView,
	FavouriteDistanceView)
from app.favourites.pages import near
from app.places.models import Place
from app.favourites.models import Favourite

urlpatterns = [
    # Services
    url(r'^Favourites/$',FavouritesListView.as_view(queryset=Favourite.objects.all(), serializer_class=FavouritePlaceSerializer), name="favoritos"),
    url(r'^Favourite/(?P<pk>[0-9]+)/$',FavouriteView.as_view(), name="favorito_delete"),
    url(r'^Favourite/$',FavouriteView.as_view(), name="favorito"),
    url(r'^DistancePlaceFavourite/$',FavouriteDistanceView.as_view(), name="dist"),
]