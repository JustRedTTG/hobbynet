#!/usr/bin/env sh

source venv/bin/activate
pip freeze > requirements.txt
deactivate
