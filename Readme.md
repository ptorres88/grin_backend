# Prueba Grin


Exposición y consumo de API para lugares de interés dado una localidad.

## Stack

* python 3.4
* django
* django rest framework

## Decisiones de Diseño e Implementación.

### Postgresql
Debido a la extensión que se determinó usar POSTGIS
### Django
Debido a la cantidad de extensiones que puede manejar para diversos
escenarios.
### Docker
Para la creación de una imagen y poder hacer un ambiente simulado de producción con Heroku


## Extensiones de django y python

* Memcached
Para uso de cache

* django-rest-swagger
Para documentación de API

* djangorestframework
Para extender django con REST

* Fabric3
Para creación de imagen y deploy

## Base de datos

A continuación se muestran las tablas (modelos) que se usaron

 Schema |            Name            | Type  |  Owner  
--------|----------------------------|-------|---------
 public | auth_user                  | table | backend
 public | favourites_favourite       | table | backend
 public | places_place               | table | backend
 public | spatial_ref_sys            | table | backend

Donde el esquema de places:

Column   | Type 
-------------|-----------------------
 id          | integer 
 name        | character varying(128)
 pos         | geometry(Point,4326)
 popularity  | double precision 
 description | character varying(256)
 user_id     | integer

Y el esquema de favourites:

   Column    |          Type          |
-------------|------------------------|
 id          | integer                |
 user_id     | integer                |
 description | character varying(256) |
 distance    | double precision       |
 name        | character varying(128) |
 popularity  | double precision       |
 pos         | geometry(Point,4326)   |


# Despliegue en local

* una vez que se clona el repositorio crear un ambiente virtual con venv
* `pip3 install -r requirements.txt`
* activar el ambiente `source env/bin/activate`
* `python manage.py makemigrations``
* `python manage.py migrate`
* Xorrer pruebas unitarias `python manage.py test`


# Despliegue automático en ambiente prod
* activar el ambiente virtual source env/bin/activate
* fab run

Es necesairo hacer login con heroku
* `heroku login`

* El archivo .env contiene las variables de ambiente y no debe agregarse a git, 

# Despliegue manual en embiente prod

`docker build --tag web_image .`

probar en local:   `docker run  -p 8000:8000 --env-file .env web_image`

`docker exec -it web_image bash`

`python3 manage.py makemigrations`

`python3 manage.py migrate`

`python3 manage.py test app`

`heroku container:login`

`heroku container:push web -a grin-app`

`heroku container:release web -a grin-app`
`heroku open -a grin-app`


# API

## Documentación

La documentación se puede ver en /docs/

## Endpoints y prueba usando POSTMAN


##### Documentación con swagger
![alt text](http://i67.tinypic.com/2w6s93t.png)
##### Endpoints con swagger
![alt text](http://i67.tinypic.com/18k9c9.png)
##### Alta usuario
![alt text](http://i68.tinypic.com/4sfup2.png)
##### Login incorrecto (400)
![alt text](http://i65.tinypic.com/161yu1f.png)
##### Login (200)
![alt text](http://i65.tinypic.com/33enbds.png)
##### Token requerido para otros endpoints
![alt text](http://i67.tinypic.com/2ebsh20.png)
##### Vista de marcar lugar
![alt text](http://i67.tinypic.com/2rylfo9.png)
##### Vista de login
![alt text](http://i67.tinypic.com/2czsw75.png)
##### Vista de nuevo usuario
![alt text](http://i63.tinypic.com/67m91v.png)
##### Vista de dashboard
![alt text](http://i65.tinypic.com/2lm76l3.png)
##### Lugares cercanos (foursquare)
![alt text](http://i68.tinypic.com/wvvd4h.png)
##### Lugares favoritos
![alt text](http://i64.tinypic.com/2qjygt1.png)
##### Endpoint sin lugar ingresado
![alt text](http://i64.tinypic.com/33fba0p.png)
##### Endpoint paginado de lugares

Nota: El ordenamiento en este endpoint se hizo por código ordenando diccionarios debido a que no encontré una forma de obtenerlos desde los endpoints de foursquare
![alt text](http://i67.tinypic.com/35k7q1g.png)

##### Endpoint paginación, sortkey de lugares favoritos
![alt text](http://i64.tinypic.com/wsmmub.png)


