from io import BytesIO

from aiohttp.web import Response as send_file
from PIL import Image

from utils import http
from utils.endpoint import Endpoint


class Spank(Endpoint):
    async def generate(self, request, avatars, text, usernames):
        base = Image.open('assets/spank/spank.jpg').resize((500, 500))
        img1 = Image.open(await http.get_image(request, avatars[0])).resize((140, 140)).convert('RGBA')
        img2 = Image.open(await http.get_image(request, avatars[1])).resize((120, 120)).convert('RGBA')
        base.paste(img1, (225, 5), img1)
        base.paste(img2, (350, 220), img2)

        b = BytesIO()
        base.save(b, format='png')
        b.seek(0)
        return send_file(body=b, content_type='image/png')


def setup():
    return Spank()
