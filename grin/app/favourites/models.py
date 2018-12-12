# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.gis.db import models
from django.contrib.auth.models import User

class Favourite(models.Model):
	
    """
    Includes foursquare info and distance from place object
    """

    name = models.CharField(max_length = 128, blank=True)
    pos = models.PointField()
    popularity = models.FloatField()
    description = models.CharField(max_length = 256, null=True, default='Unknown')
    distance = models.FloatField()
    user = models.ForeignKey(User, default = None,  on_delete=models.CASCADE)