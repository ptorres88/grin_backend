# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from django.urls import path
from app.places.views import PlaceView, NearbyPlacesView

urlpatterns = [
    # Services
    url(r'^Place/$',PlaceView.as_view(), name="place"),
    url(r'^Places/$',NearbyPlacesView.as_view(), name="nearly places"),
]