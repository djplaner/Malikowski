import json

from sqlalchemy.engine.url import URL 
from sqlalchemy import create_engine

import os
import sys

CONFIG_DIR="/Users/david/.ipython"

def connect():

    CONFIG=CONFIG_DIR+'/config.json';

    with open(CONFIG) as f:
        conf = json.load(f)

    engine = create_engine(URL(**conf))

    return engine


def config():
    CONFIG=CONFIG_DIR+'/lms.json';

    with open(CONFIG) as f:
        conf = json.load(f)

    return conf


if __name__ == '__main__':
    connect()
