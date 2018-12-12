# -*- coding: utf-8 -*-

from django.shortcuts import render

def near(request):
    return render(request, 'near.html')