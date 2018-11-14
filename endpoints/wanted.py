from io import BytesIO

from aiohttp.web import Response as send_file
from PIL import Image

from utils import http
from utils.endpoint import Endpoint


class Wanted(Endpoint):
    async def generate(self, request, avatars, text, usernames):
        base = Image.open('assets/wanted/wanted.png').convert('RGBA')
        avatar = Image.open(await http.get_image(request, avatars[0])).resize((447, 447)).convert('RGBA')
        base.paste(avatar, (145, 282), avatar)

        b = BytesIO()
        base.save(b, format='png')
        b.seek(0)
        return send_file(body=b, content_type='image/png')


def setup():
    return Wanted()
