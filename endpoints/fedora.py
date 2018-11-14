from io import BytesIO

from PIL import Image
from aiohttp.web import Response as send_file

from utils import http
from utils.endpoint import Endpoint


class Fedora(Endpoint):
    async def generate(self, request, avatars, text, usernames):
        base = Image.open('assets/fedora/fedora.png').convert('RGBA')
        avatar = Image.open(await http.get_image(request, avatars[0])).resize((275, 275)).convert('RGBA')
        final_image = Image.new('RGBA', base.size)

        # Put the base over the avatar
        final_image.paste(avatar, (112, 101), avatar)
        final_image.paste(base, (0, 0), base)

        b = BytesIO()
        final_image.save(b, format='png')
        b.seek(0)
        return send_file(body=b, content_type='image/png')


def setup():
    return Fedora()
