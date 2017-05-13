import json

from sqlalchemy.engine.url import URL 
from sqlalchemy import create_engine

import os
import sys

#-- update this to point to where you config.json and lms.json files are
CONFIG_DIR="/Users/david/.ipython"

#-- create database connection
def connect():
    CONFIG=CONFIG_DIR+'/config.json';

    try:
        with open(CONFIG) as f:
            conf = json.load(f)

    except IOError:
        sys.exit( "could not open file " + CONFIG )

    engine = create_engine(URL(**conf))

    return engine

#-- grab site specific Moodle/database settings (e.g. mdl_prefix)
def config():
    CONFIG=CONFIG_DIR+'/lms.json';

    try:
        with open(CONFIG) as f:
            conf = json.load(f)

    except IOError:
        sys.exit( "could not open file " + CONFIG )

    return conf


if __name__ == '__main__':
    connect()
