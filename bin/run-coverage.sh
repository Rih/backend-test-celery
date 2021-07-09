#!/usr/bin/env bash

coverage3 run --source='.' manage.py test
coverage3 report -m > $1