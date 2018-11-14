from io import BytesIO

from aiohttp.web import Response as send_file
from PIL import Image

from utils import http
from utils.endpoint import Endpoint


class SickBan(Endpoint):
    async def generate(self, request, avatars, text, usernames):
        base = Image.open('assets/ban/ban.png').convert('RGBA')
        avatar = Image.open(await http.get_image(request, avatars[0])).resize((400, 400)).convert('RGBA')
        base.paste(avatar, (70, 344), avatar)

        b = BytesIO()
        base.save(b, format='png')
        b.seek(0)
        return send_file(body=b, content_type='image/png')


def setup():
    return SickBan()
