FROM ubuntu:16.04
  
RUN apt-get update
RUN apt-get install -y libpq-dev python3-dev build-essential python-setuptools python3-pip git libcurl4-openssl-dev libssl-dev libffi-dev
RUN mkdir /grin
WORKDIR /grin

ADD requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

ADD set_prod_env.sh set_prod_env.sh
CMD [".", "set_prod_env.sh"]
RUN apt-get install -y binutils libproj-dev gdal-bin

ADD grin grin/
ADD .git .git/

# Run the app.  CMD is required to run on Heroku
WORKDIR /grin/grin
CMD python3 manage.py runserver 0.0.0.0:$PORT