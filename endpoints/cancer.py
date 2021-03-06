from io import BytesIO

from PIL import Image
from aiohttp.web import Response as send_file

from utils import http
from utils.endpoint import Endpoint


class Cancer(Endpoint):
    async def generate(self, request, avatars, text, usernames):
        base = Image.open('assets/cancer/cancer.png').convert('RGBA')
        avatar = Image.open(await http.get_image(request, avatars[0])).resize((100, 100)).convert('RGBA')

        base.paste(avatar, (351, 200), avatar)

        b = BytesIO()
        base.save(b, format='png')
        b.seek(0)
        return send_file(body=b, content_type='image/png')


def setup():
    return Cancer()
