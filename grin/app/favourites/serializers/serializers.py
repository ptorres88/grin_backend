# -*- coding: utf-8 -*-

from rest_framework import serializers
from app.favourites.models import Favourite

class FavouritePlaceSerializer(serializers.ModelSerializer):
   
	"""
	Pagination basic setup
	"""

	class Meta:
		model = Favourite
		fields = ('id', 'name', 'popularity', 'description', 'distance')

class FavouriteViewSerializer(serializers.ModelSerializer):
	class Meta:
		model = Favourite
		fields = ('name','popularity','description')

class FavouriteDistanceSerializer(serializers.ModelSerializer):
	class Meta:
		model = Favourite
		fields = ()