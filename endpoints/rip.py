from io import BytesIO

from PIL import Image
from aiohttp.web import Response as send_file

from utils import http
from utils.endpoint import Endpoint


class Rip(Endpoint):
    async def generate(self, request, avatars, text, usernames):
        base = Image.open('assets/rip/rip.png').convert('RGBA').resize((642, 806))
        avatar = Image.open(await http.get_image(request, avatars[0])).resize((300, 300)).convert('RGBA')

        base.paste(avatar, (175, 385), avatar)

        b = BytesIO()
        base.save(b, format='png')
        b.seek(0)
        return send_file(body=b, content_type='image/png')


def setup():
    return Rip()
