# Dockerfile

FROM docker.io/library/python:3.13-slim-bookworm

RUN apt-get update -y && apt-get clean

WORKDIR /blog

COPY ./app ./app

COPY ./setup.py .

COPY ./start_blog.sh .

COPY ./requirements.txt .

RUN chmod +x ./start_blog.sh

RUN pip install --no-cache-dir waitress -r requirements.txt

EXPOSE 5000

CMD ["./start_blog.sh"]
