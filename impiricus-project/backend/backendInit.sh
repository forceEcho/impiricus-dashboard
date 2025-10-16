#! /usr/bin/env bash

set -e
set -x

# initialize database
python app/db_prestart.py