# Dockerfile

### builder image
FROM docker.io/library/python:3.13-slim-bookworm AS builder-image

RUN apt-get update -y && apt-get install -y --no-install-recommends build-essential gcc

RUN python -m venv /blog/venv
ENV PATH="/blog/venv/bin:$PATH"

WORKDIR /blog

COPY ./requirements.txt .

COPY ./app ./app

COPY ./setup.py .

COPY ./init_db.sh .

RUN chmod +x ./init_db.sh

RUN pip install --no-cache-dir waitress -r requirements.txt

### deploy image

FROM docker.io/library/python:3.13-slim-bookworm AS final-image

RUN apt-get update -y

RUN apt-get clean && rm -rf /var/lib/apt/lists/*

ENV PATH="/blog/venv/bin:$PATH"

COPY --from=builder-image /blog /blog

WORKDIR /blog

RUN ./init_db.sh

EXPOSE 5000

CMD ["waitress-serve", "--port=5000", "--threads=1", "--call", "app:create_app"]
