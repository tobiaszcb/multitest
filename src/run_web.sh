#!/bin/bash
echo "Setting up"
echo "Copying geckodriver to /usr/local/bin"
cp ./geckodriver /usr/local/bin/
echo "Installing firefox (iceweasel)"
apt update
apt -y install less vim  iceweasel
echo "Starting celery in the background"
celery -A multitest worker -l info &
echo "Starting django server"
python3 manage.py runserver 0.0.0.0:8000
