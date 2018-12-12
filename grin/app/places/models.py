# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.conf import settings

class Place(models.Model):
	
	""" 
	Place where user is settled (one per user)
	"""
	
	name = models.CharField(max_length = 128)
	pos = models.PointField()
	popularity = models.FloatField()
	description = models.CharField(max_length = 256, null=True, default='Unknown')
	user = models.OneToOneField(User, default = None, on_delete=models.CASCADE)
