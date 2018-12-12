# -*- coding: utf-8 -*-

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.contrib.gis.geos import Point

class AccountTests(APITestCase):

	def setUp(self):
		self.user_data = {'username': 'megauser'}

	def get_user(self):
		user = User.objects.create_user(self.user_data['username'], self.user_data['username'])
		self.client.force_authenticate(user)

    # create new place
	def test_favourites(self):
		self.get_user()

		url = 'http://localhost:8000/api/Place/'
		lat = 19.3795049
		lng = -99.1423947
		name = 'metro nativitas'
		popularity = 1.1
		description = 'metro linea 2'
		response = self.client.post(url, {'lat':lat,'lng':lng,'name':name,
        	'popularity':popularity,'description':description})
		
		url = 'http://localhost:8000/api/Favourite/'
		name = 'metro chabacano'
		popularity = 1.5
		description = 'metro linea 2 y 8'
		lat = 19.4087181
		lng = -99.1377711
		distance = 0
		response2 = self.client.post(url, {'lat':lat,'lng':lng,'name':name,
        	'popularity':popularity,'description':description,
        	'distance':distance})
		
		url = 'http://localhost:8000/api/DistancePlaceFavourite/'
		response3 = self.client.put(url)

		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(response2.status_code, status.HTTP_201_CREATED)
		self.assertEqual(response3.status_code, status.HTTP_200_OK)