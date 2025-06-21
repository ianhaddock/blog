#!/usr/bin/env bash
set -e

if [ ! -s '/blog/instance/blogapp.sqlite' ]; then
    flask --app app init-db
fi
