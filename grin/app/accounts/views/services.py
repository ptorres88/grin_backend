# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# Required for swagger, besides serializer
from rest_framework.generics import GenericAPIView
from django.contrib.auth.models import User
from app.accounts.serializers.serializer import UserViewSerializer

class UserView(GenericAPIView):

	"""
	Registra un nuevo usuario
	"""

	serializer_class = UserViewSerializer

	def post(self, request):
		
		username = request.POST.get('username', '')
		password = request.POST.get('password', '')

		if username and password:

			try:
				description =  'ok'
				status_code = status.HTTP_201_CREATED
				email = username
				user = User.objects.create_user(username, email, password)
			except IntegrityError as e:
				description = e
				status_code = status.HTTP_400_BAD_REQUEST
		else:
			description =  'user not created'
			status_code = status.HTTP_400_BAD_REQUEST

		return Response({'msg': description }, status = status_code)


class LoginView(GenericAPIView):

	"""
	Autentica y hace login de usuario
	"""
	
	serializer_class = UserViewSerializer

	def post(self, request):
		user = authenticate(username=request.POST.get('username',''), 
			password=request.POST.get('password',''))
		if user is not None:
			login(request, user)
			return Response({"msg" : "welcome"}, status=status.HTTP_200_OK)
		else:
			return Response({"msg" : "something went wrong"}, status=status.HTTP_400_BAD_REQUEST)
			

class LogoutView(APIView):
    
	"""
	Logout de usuario
	"""

	permission_classes = (IsAuthenticated,)

	def get(self, request):
		logout(request)
		return Response({"msg":"ok"},status=status.HTTP_200_OK, template_name="home")
