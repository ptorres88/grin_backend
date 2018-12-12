# -*- coding: utf-8 -*-

from rest_framework import serializers

class PointField(serializers.Field):
	"""
	Needed for lat lng tuple
	"""
	def to_representation(self, value):
		return {value.x, value.y}

class PlaceSerializer(serializers.Serializer):
    name = serializers.CharField()
    pos = PointField()
    popularity = serializers.FloatField()

class NearPlacesSerializer(serializers.Serializer):
	lat = serializers.FloatField()
	lng = serializers.FloatField()