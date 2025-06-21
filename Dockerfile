# Dockerfile

FROM docker.io/library/python:3.13-slim-bookworm

RUN apt-get update -y && apt-get clean

WORKDIR /blog

COPY ./requirements.txt .

RUN pip install --no-cache-dir waitress -r requirements.txt

COPY ./app ./app

COPY ./setup.py .

COPY ./init_db.sh .

RUN chmod +x ./init_db.sh

RUN ./init_db.sh

EXPOSE 5000

CMD ["waitress-serve", "--port=5000", "--threads=1", "--call", "app:create_app"]
