from io import BytesIO

from aiohttp.web import Response as send_file
from PIL import Image

from utils import http
from utils.endpoint import Endpoint


class Jail(Endpoint):
    async def generate(self, request, avatars, text, usernames):
        overlay = Image.open('assets/jail/jail.png').resize((350, 350))
        base = Image.open(await http.get_image(request, avatars[0])).convert('LA').resize((350, 350))
        base.paste(overlay, (0, 0), overlay)

        b = BytesIO()
        base.save(b, format='png')
        b.seek(0)
        return send_file(body=b, content_type='image/png')


def setup():
    return Jail()
