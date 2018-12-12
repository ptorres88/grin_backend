# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from django.urls import path
from app.accounts.views.services import LoginView, LogoutView, UserView
#from app.accounts.pages import home

urlpatterns = [
    # Services
    url(r'^Login/$',LoginView.as_view(), name="login"),
    url(r'^Logout/$', LogoutView.as_view(), name='logout'),
    url(r'^User/$', UserView.as_view(), name='create user'),
]