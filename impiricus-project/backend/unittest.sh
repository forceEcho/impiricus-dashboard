#! /usr/bin/env bash
set -e
set -x

python app/db_prestart.py

python -m pytest tests/