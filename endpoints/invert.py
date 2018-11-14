from io import BytesIO

from aiohttp.web import Response as send_file
from PIL import Image, ImageOps

from utils import http
from utils.endpoint import Endpoint


class Invert(Endpoint):
    async def generate(self, request, avatars, text, usernames):
        img = Image.open(await http.get_image(request, avatars[0]))
        if img.mode == 'RGBA':
            r, g, b, a = img.split()
            rgb_image = Image.merge('RGB', (r, g, b))
            inverted = ImageOps.invert(rgb_image)
            r, g, b = inverted.split()
            img = Image.merge('RGBA', (r, g, b, a))
        else:
            img = ImageOps.invert(img)

        b = BytesIO()
        img.save(b, format='png')
        b.seek(0)
        return send_file(body=b, content_type='image/png')


def setup():
    return Invert()
