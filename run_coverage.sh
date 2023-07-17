#!/usr/bin/env sh

source venv/bin/activate
coverage run manage.py test --parallel 6 --noinput
coverage report
deactivate
