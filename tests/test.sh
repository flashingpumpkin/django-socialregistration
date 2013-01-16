#!/bin/bash

export PYTHONPATH=$PWD/../:$PYTHONPATH

django-admin.py test facebook foursquare twitter github instagram linkedin openid tumblr twitter --settings tests.settings
