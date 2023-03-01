# Dockerfile

FROM python:3.8

WORKDIR /app

COPY ./app .

COPY ./setup.py .

COPY ./start_blog.sh .

COPY ./requirements.txt .

RUN chmod +x ./start_blog.sh

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["./start_blog.sh"]
