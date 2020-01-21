Docker Workshop
===============

Exercise
--------

Build dash app with a file upload feature, and send the files to an ML api
for classification.

The python code is provided; the exercise is to write the Dockerfiles and
docker-compose.yml file that tie the system together

Suggestions
-----------

1. Run the dash app with

> CMD ["python3", "/app/main.py"] 


2. Use this base image for the mlapi

> frolvlad/alpine-python-machinelearning

You'll want to install `fastapi`.
