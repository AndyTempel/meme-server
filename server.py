import argparse
import asyncio
import json
import platform
import traceback
from concurrent.futures.thread import ThreadPoolExecutor

import aiohttp
import aiofiles
import aiohttp_debugtoolbar
import aiohttp_jinja2
import jinja2
from aiohttp import web

import endpoints
from utils.ratelimits import ratelimit

# if platform.system() != "Windows":
#     import uvloop
#     asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

parser = argparse.ArgumentParser(description="Dank Memer image generation fork - rewritten in async by NANI#0001")
parser.add_argument('--path')
parser.add_argument('--port')
io_pool_exc = ThreadPoolExecutor()
route = web.RouteTableDef()


async def get_auth_keys():
    try:
        async with aiofiles.open('keys.json', executor=io_pool_exc) as file:
            data = json.loads(await file.read())
            if not isinstance(data, list):
                print('keys.json must only contain an array of valid auth tokens')
                return []
            else:
                return data
    except FileNotFoundError:
        print('keys.json wasn\'t found in the current directory')
        return []

rdb = r.connect(RDB_ADDRESS, RDB_PORT, db=RDB_DB)

@route.get('/')
@aiohttp_jinja2.template("index.html")
async def index(request):
    data = {}
    sorted_data = {}

    for endpoint in endpoints.endpoints:
        data[endpoint] = {'hits': endpoints.endpoints[endpoint].hits,
                          'avg_gen_time': endpoints.endpoints[endpoint].get_avg_gen_time()}

    for i in sorted(data.keys(), key=lambda x: x.lower()):
        sorted_data[i] = data[i]

    return {"data": sorted_data}


@route.get('/api/{endpoint}')
async def api(request):
    if request.headers.get('authorization') is None:
        return web.json_response({"error": True, "message": "Forbidden"}, status=403)
    else:
        if request.headers.get('authorization') not in await get_auth_keys():
            return web.json_response({"error": True, "message": "Forbidden"}, status=403)
    endpoint = request.match_info.get('endpoint', None)
    if endpoint not in endpoints.endpoints:
        return web.json_response({'status': 404, 'error': 'Endpoint {} not found!'.format(endpoint)})

    try:
        result = await endpoints.endpoints[endpoint].run(request=request, text=request.query.getone('text', ''),
                                                         avatars=[request.query.getone('avatar1', ''),
                                                                  request.query.getone('avatar2', '')],
                                                         usernames=[request.query.getone('username1', ''),
                                                                    request.query.getone('username2', '')])
    except Exception as e:
        print(e, ''.join(traceback.format_tb(e.__traceback__)))
        result = web.json_response({'status': 500, 'error': str(e)})
    return result


async def init_app():
    app = web.Application()
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('./views'))
    if platform.system() == "Windows":
        aiohttp_debugtoolbar.setup(app)
    app['client_session'] = aiohttp.ClientSession(headers={"User-Agent": "RickBot-ImageGeneration/0.0.1a"})
    app.router.add_routes(route)
    return app

if __name__ == '__main__':
    args = parser.parse_args()
    if platform.system() == "Windows":
        web.run_app(init_app(), host="127.0.0.1", port=5000, access_log=True)
    else:
        web.run_app(init_app(), path=args.path)
