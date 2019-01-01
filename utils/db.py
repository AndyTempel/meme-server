try:
    import ujson as json
except ImportError:
    import json

import rethinkdb as r
import redis
from flask import g
from utils.rethink import Rethink
from utils.mongo import Mongo
config = json.load(open('config.json'))


REDIS_ADDRESS = config.get('redis_address', 'localhost')
REDIS_PORT = config.get('redis_port', 6379)
REDIS_DB = config.get('redis_db', 1)


def get_db():
    if config['db'] == 'rethink':
        if 'rethink' not in g:
            g.rethink = Rethink()
        return g.rethink
    elif config['db'] == 'mongo':
        if 'mongo' not in g:
            g.mongo = Mongo()
        return g.mongo


def get_redis():
    if 'redis' not in g:
        g.redis = redis.Redis(host=REDIS_ADDRESS, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)
    return g.redis
