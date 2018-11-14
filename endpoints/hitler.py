from io import BytesIO

from aiohttp.web import Response as send_file
from PIL import Image

from utils import http
from utils.endpoint import Endpoint


class Hitler(Endpoint):
    async def generate(self, request, avatars, text, usernames):
        base = Image.open('assets/hitler/hitler.jpeg')
        img1 = Image.open(await http.get_image(request, avatars[0])).convert('RGBA').resize((140, 140))
        base.paste(img1, (46, 43), img1)

        b = BytesIO()
        base.save(b, format='png')
        b.seek(0)
        return send_file(body=b, content_type='image/png')


def setup():
    return Hitler()
