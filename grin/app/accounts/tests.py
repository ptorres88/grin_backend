# -*- coding: utf-8 -*-

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User

class AccountTests(APITestCase):

	def setUp(self):
		self.user_data = {'username': 'juan','password' :'123456'}

    # create new account
	def test_create_account(self):
		url = 'http://localhost:8000/api/User/'
		response = self.client.post(url, self.user_data)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

	# bad auth
	def test_login_should_return_400(self):
		url = 'http://localhost:8000/api/Login/'
		data = {'username': 'pedro', 'password':'no'}
		response = self.client.post(url, data)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	# good auth
	def test_login_should_return_201(self):
		url = 'http://localhost:8000/api/User/'
		response = self.client.post(url, self.user_data)
		url = 'http://localhost:8000/api/Login/'
		response2 = self.client.post(url, self.user_data)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(response2.status_code, status.HTTP_200_OK)
	
	# logout
	def test_logout_should_return_ok(self):
		user = User.objects.create_user(self.user_data['username'], self.user_data['username'])
		self.client.force_authenticate(user)
		url = 'http://localhost:8000/api/Logout/'
		response = self.client.get(url)
		self.assertEqual(response.data['msg'], 'ok')

	# unauthorized since no authentication 
	def test_logout_should_return_401(self):
		user = User.objects.create_user(self.user_data['username'], self.user_data['username'])
		url = 'http://localhost:8000/api/Logout/'
		response = self.client.get(url)
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
		
        