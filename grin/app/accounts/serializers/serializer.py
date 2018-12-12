# -*- coding: utf-8 -*-

from rest_framework import serializers
from django.contrib.auth.models import User


class UserViewSerializer(serializers.ModelSerializer):

	"""
	Only needed for auth & signup
	"""

	class Meta:
		model = User
		fields = ('username','password')