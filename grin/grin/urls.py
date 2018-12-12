"""
grin_backend URL Configuration
"""

from django.contrib import admin
from django.urls import path
from django.urls import include
from django.views.generic.base import TemplateView
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import renderers
from rest_framework_swagger.views import get_swagger_view
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer
from rest_framework.authtoken import views
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.schemas import SchemaGenerator
from rest_framework.views import APIView
from rest_framework_swagger import renderers
from app.accounts.views.services import LoginView, LogoutView

admin.autodiscover()

# Swagger for REST API documentation

class SwaggerSchemaView(APIView):

    """
    Custom schema for endpoints that require auth
    """

    permission_classes = [AllowAny]
    renderer_classes = [
        renderers.OpenAPIRenderer,
        renderers.SwaggerUIRenderer
    ]

    def get(self, request):
        generator = SchemaGenerator()
        schema = generator.get_schema(request=None)

        return Response(schema)

urlpatterns = [

    # Index and admin views
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='login.html'), name='home'),

    # General views of project (dashboard)
    path('accounts/', include('django.contrib.auth.urls')),
    path('places/', TemplateView.as_view(template_name='search.html'), name='place'),
    path('near/',TemplateView.as_view(template_name='near.html'), name="near"),
    path('register/',TemplateView.as_view(template_name='register.html'), name="new"),

    # Services, API router
    url(r'^api/', include(('app.accounts.urls_api','accounts_api'), namespace='accounts')),
    url(r'^api/', include(('app.places.urls','places'), namespace='places')),
    url(r'^api/', include(('app.favourites.urls','favourites'), namespace='favourites')),
    path('api-auth-token/', views.obtain_auth_token, name='api-auth-token'),

    
    # Documentation
    url(r'^docs/$', SwaggerSchemaView.as_view()),
]
