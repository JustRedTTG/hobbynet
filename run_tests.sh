#!/usr/bin/env sh

source venv/bin/activate
python manage.py test --parallel 6 --noinput
deactivate
