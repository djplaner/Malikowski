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

    with open(CONFIG) as f:
        conf = json.load(f)

    engine = create_engine(URL(**conf))

    return engine

#-- grab site specific Moodle/database settings (e.g. mdl_prefix)
def config():
    CONFIG=CONFIG_DIR+'/lms.json';

    with open(CONFIG) as f:
        conf = json.load(f)

    return conf


if __name__ == '__main__':
    connect()
