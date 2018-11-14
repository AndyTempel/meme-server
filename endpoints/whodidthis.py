from io import BytesIO

from aiohttp.web import Response as send_file
from PIL import Image

from utils import http
from utils.endpoint import Endpoint


class Whodidthis(Endpoint):
    async def generate(self, request, avatars, text, usernames):
        base = Image.open('assets/whodidthis/whodidthis.png')
        avatar = Image.open(await http.get_image(request, avatars[0])).resize((720, 405)).convert('RGBA')
        base.paste(avatar, (0, 159), avatar)

        b = BytesIO()
        base.save(b, format='png')
        b.seek(0)
        return send_file(body=b, content_type='image/png')


def setup():
    return Whodidthis()
