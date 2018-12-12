# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf import settings
from django.shortcuts import render
from django.contrib.gis.geos import Point

from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from rest_framework.generics import GenericAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters

from app.places.models import Place
from app.favourites.models import Favourite
from app.favourites.serializers.serializers import (FavouritePlaceSerializer,
	FavouriteViewSerializer,
	FavouriteDistanceSerializer)


class TenItemsSetPagination(PageNumberPagination):
	page_size = settings.PAGINATION_SIZE


class NotPaginatedSetPagination(PageNumberPagination):
	page_size = None

class FavouritesListView(ListAPIView):

	"""
	Lista de lugares favoritos
	"""
	
	pagination_class = TenItemsSetPagination
	queryset = Favourite.objects.all()
	serializer_class = FavouritePlaceSerializer
	filter_backends = (filters.OrderingFilter,)
	ordering_fields = ('name', 'distance', 'popularity')
	ordering = ('name',)


class FavouriteView(GenericAPIView):

	"""
	Registra un lugar favorito
	"""

	permission_classes = (IsAuthenticated,)
	serializer_class = FavouriteViewSerializer
	
	def post(self, request):
		name = request.POST.get('name','')
		popularity = request.POST.get('popularity','')
		description = request.POST.get('description','')
		lat = request.POST.get('lat','')
		lng = request.POST.get('lng','')
		pos = Point(float(lat), float(lng))
		distance = request.POST.get('distance',0)
		favourite = Favourite.objects.create(name=name, popularity = popularity, 
			description = description, distance = distance,
			pos = pos, user = request.user)
		return Response({'msg' : 'ok'}, status = status.HTTP_201_CREATED)

	def put(self, request, pk):
		favourite = Favourite.objects.get(pk = pk)
		favourite.delete()
		return Response({'msg' : 'ok'}, status = status.HTTP_200_OK)

class FavouriteDistanceView(GenericAPIView):

	"""
	Recalcula la distancia en km respecto al lugar del usuario
	"""

	permission_classes = (IsAuthenticated,)
	serializer_class = FavouriteDistanceSerializer
	
	def put(self, request):
		user = request.user
		place = Place.objects.get(user = user)
		pos_a = place.pos
		favourites = Favourite.objects.filter(user = user)

		if favourites.exists:
			for fav in favourites:
				pos_b = fav.pos
				dist_km = pos_a.distance(pos_b)*100
				fav.distance = dist_km
				fav.save()

		return Response({'msg' : 'ok'}, status = status.HTTP_200_OK)