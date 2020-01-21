#FROM tiangolo/uwsgi-nginx-flask:python3.6-alpine3.8
FROM python:3-alpine

RUN apk add build-base gcc

RUN pip3 install --upgrade pip
RUN pip3 install dash
RUN pip3 install dash-renderer
RUN pip3 install dash-html-components
RUN pip3 install dash-core-components
RUN pip3 install plotly --upgrade
#RUN pip3 install fastapi

#CMD ["tail", "-F", "/dev/null"]

CMD ["python", "/app/main.py"]
