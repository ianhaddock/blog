[![Docker Image CI](https://github.com/ianhaddock/blog/actions/workflows/docker-image-ci.yml/badge.svg)](https://github.com/ianhaddock/blog/actions/workflows/docker-image-ci.yml)

# Blog
Lightweight blog app used on my site, [ianhaddock.com][1]. 

<p align="center">
  <img width="90%" height="auto" src="readme.jpg">
</p>

## Uses
* Python
* Flask
* sqlite3
* Markdown

## Setup
Run the docker image:

```
docker run \
  -d \
  --name blog-app \
  -v "instance:/blog/instance" \
  -p 8080:5000 \
  ghcr.io/ianhaddock/blog:latest
```

Or run directly:

```
# create a virtual environment
$ python -m venv venv

# enable virtual environment
$ . venv/bin/activate 

# pull the latest
$ git pull https://github.com/ianhaddock/blog.git

# install wsgi (e.g. waitress) and requirements
$ pip install waitress -r requirements.txt

# setup 
$ flask --app app init-db

# start 
$ waitress-serve --port=8080 --call app:create_app 
```

## Sources
Started with a [tutorial on Flask][1] and decided to continue. 


[1]: https://blog.ianhaddock.com
[2]: https://flask.palletsprojects.com/en/2.2.x/tutorial/ 
