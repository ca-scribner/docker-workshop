Docker Workshop
===============

Written for Statistics Canada 

*Blair Drummond, January 2020*

Exercise
--------

Build dash app with a file upload feature, and send the files to an ML api
for classification.

The python code is provided; the exercise is to write the Dockerfiles and
docker-compose.yml file that tie the system together


Getting Started
---------------

1. Install Docker

- Windows: go to [the docker toolbox downloads](github.com/docker/toolbox/releases)
- Ubuntu: [download instructions](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-18-04)
- Redhat: [download instructions](https://www.cyberciti.biz/faq/install-use-setup-docker-on-rhel7-centos7-linux/)

2. Install docker-compose with `pip install --user docker-compose`

3. Download this repository. 

Exercises
---------

1. Try to run the dash app with `docker-compose up`...

Then test the app on `localhost:8888`

2. Try to come up with a new model for the classification and integrate it.

3. How would you make the storage persistent?

4. **HARD:** Figure out how to use a production-grade webserver (`uwsgi` or `gunicorn`)
