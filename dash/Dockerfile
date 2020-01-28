FROM python:3.8-alpine

RUN pip install --upgrade pip

WORKDIR /app/dash

COPY requirements.txt /app/dash/requirements.txt

RUN pip install -r requirements.txt

# Need COPY of dash file or use by volumes:
# docker run -v $(pwd):/app/dash imagename

CMD ["python", "/app/dash/app/main.py"]