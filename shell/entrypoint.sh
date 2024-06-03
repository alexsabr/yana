#!/usr/bin/bash
set -euf

. .venv/bin/activate && \
printf "venv activate \n" && \
python3 manage.py makemigrations && \
printf "migrations created \n" && \
python3 manage.py migrate && \
printf "migration ran \n" && \
httpd-foreground




