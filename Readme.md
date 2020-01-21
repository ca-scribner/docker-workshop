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

2. Download this repository.

Suggestions
-----------

1. Run the dash app with

```
CMD ["python3", "/app/main.py"] 
```

**Run this on on port 8888**


2. Run the mlapi app with 

```
CMD ["python3", "/app/api.py"] 
```

**Run this on on port 8000**


3. Use this base image for the mlapi

```
frolvlad/alpine-python-machinelearning
```

You'll want to install `fastapi`.
