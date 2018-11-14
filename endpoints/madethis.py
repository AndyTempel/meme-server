from io import BytesIO

from aiohttp.web import Response as send_file
from PIL import Image

from utils import http
from utils.endpoint import Endpoint


class MadeThis(Endpoint):
    async def generate(self, request, avatars, text, usernames):
        base = Image.open('assets/madethis/madethis.png').convert('RGBA')
        avatar = Image.open(await http.get_image(request, avatars[0])).resize((130, 130)).convert('RGBA')
        avatar2 = Image.open(await http.get_image(request, avatars[1])).resize((111, 111)).convert('RGBA')
        base.paste(avatar, (92, 271), avatar)
        base.paste(avatar2, (422, 267), avatar2)
        base.paste(avatar2, (406, 678), avatar2)
        base.paste(avatar2, (412, 1121), avatar2)

        b = BytesIO()
        base.save(b, format='png')
        b.seek(0)
        return send_file(body=b, content_type='image/png')


def setup():
    return MadeThis()
