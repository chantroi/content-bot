#!/bin/bash
python -u main.py &
cd /app && gunicorn -b :8000 web:app