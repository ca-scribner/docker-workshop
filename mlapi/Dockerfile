FROM frolvlad/alpine-python-machinelearning

RUN apk add build-base jpeg-dev zlib-dev python3-dev  
ENV LIBRARY_PATH=/lib:/usr/lib
RUN pip3 install pillow
RUN pip3 install fastapi

CMD ["python3", "/app/api.py"]
