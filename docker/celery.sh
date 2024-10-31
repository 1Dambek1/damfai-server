#!/bin/bash

cd src


if [[ "${1}" == "celery" ]]; then
  celery --app=celery_connection.celery_connect:celery worker -l INFO -B
elif [[ "${1}" == "flower" ]]; then
  celery --app=celery_connection.celery_connect:celery flower
 fi