FROM python:3.8.1-buster

# RUN pip install --upgrade pip

WORKDIR /app/mlapi

COPY ./requirements.txt ./

RUN pip install -r requirements.txt

# I could copy the code in here, but instead I'm setting this with volumes in docker-compose/docker run
# eg: docker run -v (pwd):/app/mlapi imagename
# COPY ./src ./src
# COPY ./model ./model

CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--reload", "--port", "8000"]
# CMD ["python", "main.py"]