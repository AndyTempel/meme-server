from io import BytesIO

from aiohttp.web import Response as send_file
from PIL import Image

from utils import http
from utils.endpoint import Endpoint


class Roblox(Endpoint):
    async def generate(self, request, avatars, text, usernames):
        base = Image.open('assets/roblox/roblox.png').convert('RGBA')
        avatar = Image.open(await http.get_image(request, avatars[0])).resize((56, 74)).convert('RGBA')
        base.paste(avatar, (168, 41), avatar)

        b = BytesIO()
        base.save(b, format='png')
        b.seek(0)
        return send_file(body=b, content_type='image/png')


def setup():
    return Roblox()
