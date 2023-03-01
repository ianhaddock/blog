#!/bin/bash

if [ ! -s '/blog/instance/blogapp.sqlite' ]; then
    flask --app app init-db
fi

waitress-serve --port=5000 --threads=1 --call app:create_app
