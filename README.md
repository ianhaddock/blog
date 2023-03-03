---
gitea: none
include_toc: true
---
<p align="center">
  <img  width="551" height="320" src="http://git.ianhaddock.com/ian/blog/raw/branch/main/README_image.jpg">
</p>

# Blog
This is a lightweight blog app that I use for my site, [ianhaddock.com][1]. 

## Uses
* Python
* Flask
* sqlite3
* Markdown

## Setup
There is a Dockerfile available:

```
# pull the latest
$ git pull http://git.ianhaddock.com/ian/blog.git

# build the image
$ docker image build ./ -t blog-app

# create an instance volume
$ mkdir ./instance 

# run the image
$ docker run --name blog-app -v "instance:/blog/instance" -p8080:5000 -d blog-app
```

Or run it directly:

```
# Set a virtual environment
$ python -m venv venv

# pull the latest
$ git pull http://gitea.ianhaddock.org/ian/blog.git

# install wsgi (e.g. waitress) and requirements
$ pip install waitress -r requirements.txt

# setup 
$ flask app-init
$ flask --app app init-db

# start 
$ waitress-serve --port=8080 --call app:create_app 
```

## Sources
Started with a fun [tutorial on Flask][1] and decided to contiue building. 


[1]: https://blog.ianhaddock.com
[2]: https://flask.palletsprojects.com/en/2.2.x/tutorial/ 
