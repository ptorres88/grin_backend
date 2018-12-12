# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.conf import settings
from app.places.models import Place
from django.contrib.gis.geos import Point

import foursquare
import json

from app.places.serializers.serializer_place import PlaceSerializer,NearPlacesSerializer
from rest_framework.generics import GenericAPIView

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache import cache


class PlaceView(GenericAPIView):

    """
    Returns place if exists otherwise create a new one
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = PlaceSerializer

    @method_decorator(cache_page(60*60*2))
    def get(self, request):
        place = Place.objects.get(user=request.user.id)
        serializer = PlaceSerializer(place)
        return Response({'data': serializer.data },
                        status = status.HTTP_200_OK)        

    def post(self, request):
        lat = request.POST.get('lat', '')
        lng = request.POST.get('lng', '')
        name = request.POST.get('name', '')
        popularity = request.POST.get('popularity', 0)
        description = request.POST.get('description', '')
        place, created = Place.objects.get_or_create(user = request.user,
            defaults={'name' : name, 
            'pos' : Point(float(lat), float(lng)), 
            'popularity' : popularity})
        if not created:
            place.name = name
            place.pos = Point(float(lat), float(lng))
            place.popularity = popularity
            place.description = description
            place.save()
        return Response({'msg': 'placed spawned' }, status = status.HTTP_201_CREATED)

class NearbyPlacesView(GenericAPIView):

    """
    if no text then returns nearly places of interes
    info and distance from pin
    order by distance or popularity query api
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = NearPlacesSerializer

    def initial(self, request, *args, **kwargs):

        data = request.data

        self.n = settings.PLACES_TO_SEARCH
        self.lat = request.GET.get('lat', '')
        self.lng = request.GET.get('lng', '')
        self.query_string = request.GET.get('query', '')
        self.sort = request.GET.get('sortKey', '')
        self.key_sort = ['popularity','distance']

        if not self.lat and not self.lng:
            self.proceed = False
        else:
            self.client = foursquare.Foursquare(
                client_id=settings.FOURSQUARE_CLIENT_ID,
                client_secret=settings.FOURSQUARE_SECRET)
            self.proceed = True

    def popularity(self, n, m):
        if m == 0:
            return 0
        return n / m

    def get_record(self, result):
        name = result['name']
        lat = result['location']['lat']
        lng = result['location']['lng']
        dist = result['location']['distance']
        users_count = result['stats']['usersCount']
        checkins_count = result['stats']['checkinsCount']
        popularity = self.popularity(checkins_count, users_count)
        description = 'Unknown'
        if 'categories' in result:
            if len(result['categories']) > 0:
                description = result['categories'][0]['name']
        place_details = {}
        place_details['name'] = name
        place_details['lat'] = lat
        place_details['lng'] = lng
        place_details['distance'] = int(dist)
        place_details['popularity'] = popularity
        place_details['description'] = description
        return place_details

    def get(self, request):

        if not self.proceed:
            return Response({'msg': 'no location was provided' },
                            status = status.HTTP_400_BAD_REQUEST)

        location = '{},{}'.format(self.lat,self.lng)
        
        # caching location
        cache_key = 'location'
        cache_time = 64**2
        results = cache.get(cache_key)

        if not results:
            results = self.client.venues.search(
                params={'query': self.query_string,'ll': location})
            results = results['venues']
        cache.set(cache_key, results, cache_time)
        
        
        msg = {'data':[]}

        for result in results:
            place_details = self.get_record(result)
            msg['data'].append(place_details)

        # sorting array of dictionaries
        if self.sort in self.key_sort:
            msg['data'] = sorted(msg['data'], key=lambda k: k[self.sort])
        msg['data'] = msg['data'][:self.n]
        
        return Response(msg, status = status.HTTP_200_OK)