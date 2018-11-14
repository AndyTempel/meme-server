from io import BytesIO

from PIL import Image
from aiohttp.web import Response as send_file

from utils import http
from utils.endpoint import Endpoint


class Brazzers(Endpoint):
    async def generate(self, request, avatars, text, usernames):
        base = Image.open('assets/brazzers/brazzers.png').resize((300, 150)).convert('RGBA')
        avatar = Image.open(await http.get_image(request, avatars[0])).resize((500, 500)).convert('RGBA')

        # avatar is technically the base
        avatar.paste(base, (200, 390), base)

        b = BytesIO()
        avatar.save(b, format='png')
        b.seek(0)
        return send_file(body=b, content_type='image/png')


def setup():
    return Brazzers()
