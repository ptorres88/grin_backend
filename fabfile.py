# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from fabric.api import run
from fabric.context_managers import lcd
from fabric.operations import local

def run():
    with lcd('grin'):
        local('python manage.py makemigrations')
        local('python manage.py migrate')
        local('python manage.py test app')
        
    local('docker login',capture=True)
    local('docker build --tag web_image . -f Dockerfile')
        
    local('heroku container:login')
    local('heroku container:push web -a grin-app')
    local('heroku container:release web -a grin-app')
    local('heroku open -a grin-app')
    print('OK')
