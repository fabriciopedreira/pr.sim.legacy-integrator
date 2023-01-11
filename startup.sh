#!/bin/sh

echo "Gunicorn --- Start app!"
gunicorn -c app/internal/config/gunicorn.py app.main:application --preload