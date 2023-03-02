---
gitea: none
include_toc: true
---
<p align="center">
  <img  width="551" height="320" src="http://git.ianhaddock.com/ian/blog/raw/branch/main/README_image.jpg">
</p>

# Blog
This is a lightweight blog app that I use for my site, [blog.ianhaddock.com][1]. 

## Technologies
Project created with:
* Python 3.8
* Flask n.n
* sqlite3

## Setup
There is a Dockerfile available:

```
$ docker build ./ -n blog
$ docker run -n blog 
```

Alternatively you can run it directly:

```
$ python -m venv venv
$ git pull http://gitea.ianhaddock.org/ian/blog.git
$ pip install waitress -r requirements.txt 
$ flask app-init
$ flask --app app init-db
$ waitress-serve --port=8080 --call app:create_app 
```

## Sources
Started from a cool [tutorial on Flask][1] that I enjoyed and decided to contiue building on. 


[1]: https://blog.ianhaddock.com
[2]: https://flask.palletsprojects.com/en/2.2.x/tutorial/ 
