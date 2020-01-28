FROM python:3.8-alpine

RUN pip install --upgrade pip

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

# Need COPY of dash file or use by volumes:
# docker run -v $(pwd)/src:/app/src imagename

CMD ["python", "/app/src/main.py"]