import json
from datetime import datetime, timedelta

import requests
import jinja2
from flask import request, make_response, jsonify

from utils.db import get_db

config = json.load(open('config.json'))
render_env = jinja2.Environment(loader=jinja2.FileSystemLoader('views/emails'))


class RatelimitCache(object):
    def __init__(self, expire_time=timedelta(0, 1, 0)):
        self.expire_time = expire_time
        self.cache = {}

    def __getitem__(self, item):
        c = self.cache[item]

        now = datetime.now()
        if now - c['timestamp'] < c['expire_time']:
            return c['data']

        self.cache.pop(item)
        return 0

    def get(self, item):
        return self.__getitem__(item)

    def __contains__(self, item):
        return item in self.cache

    def __setitem__(self, key, value):
        self.cache[key] = {
            'data': value,
            'timestamp': datetime.now(),
            'expire_time': self.expire_time
        }

    def expires_on(self, item):
        c = self.cache[item]

        return c['timestamp'] + c['expire_time']

    def set(self, key, value):
        return self.__setitem__(key, value)


cache = RatelimitCache()


def ratelimit(func, max_usage=5):
    def wrapper(*args, **kwargs):
        auth = request.headers.get('authorization', None)
        key = get_db().get('keys', auth)
        if key['unlimited']:
            return make_response(
                (*func(*args, **kwargs), {'X-RateLimit-Limit': 'Unlimited',
                                          'X-RateLimit-Remaining': 'Unlimited',
                                          'X-RateLimit-Reset': 2147483647}))
        if key['id'] in cache:
            usage = cache.get(key['id'])
            if usage < max_usage:
                cache.set(key['id'], usage + 1)
                return make_response((*func(*args, **kwargs),
                                      {'X-RateLimit-Limit': max_usage,
                                       'X-RateLimit-Remaining': max_usage - usage - 1,
                                       'X-RateLimit-Reset': cache.expires_on(key['id'])}))
            else:
                ratelimit_reached = key.get('ratelimit_reached', 0) + 1
                get_db().update('keys', auth, {"ratelimit_reached": ratelimit_reached})
                if ratelimit_reached % 5 == 0:
                    if 'webhook_url' in config:
                        requests.post(config['webhook_url'],
                                      json={"embeds": [{
                                          "title": f"Application '{key['name']}' ratelimited 5 times!",
                                          "description": f"Owner: {key['owner']}\n"
                                          f"Total: {ratelimit_reached}"}]})
                    requests.post(f"https://{config['postal_host']}/api/v1/send/message", headers={
                        "X-Server-API-Key": config['postal_key']
                    }, json={
                        "to": [key['email']], "from": "RickBot Services <services@is-going-to-rickroll.me>",
                        "subject": "Rate-limit has been hit 5 times!",
                        "tag": "imggen", "html_body": render_env.get_template('rate_limit.html').render({
                            "app": key,
                            "total_hits": ratelimit_reached,
                            "client_ip": request.remote_addr
                        })
                    })
                return make_response((jsonify({'status': 429, 'error': 'You are being ratelimited'}), 429,
                                      {'X-RateLimit-Limit': max_usage,
                                       'X-RateLimit-Remaining': 0,
                                       'X-RateLimit-Reset': cache.expires_on(key['id'])}))
        else:
            cache.set(key['id'], 1)
            return make_response((*func(*args, **kwargs), {'X-RateLimit-Limit': max_usage,
                                                           'X-RateLimit-Remaining': max_usage - 1,
                                                           'X-RateLimit-Reset': cache.expires_on(key['id'])}))

    return wrapper
