from io import BytesIO

from PIL import Image
from aiohttp.web import Response as send_file

from utils import http
from utils.endpoint import Endpoint


class Door(Endpoint):
    async def generate(self, request, avatars, text, usernames):
        base = Image.open('assets/door/door.jpg').convert('RGBA')
        avatar = Image.open(await http.get_image(request, avatars[0])).resize((479, 479)).convert('RGBA')
        final_image = Image.new('RGBA', base.size)

        # Put the base over the avatar
        final_image.paste(avatar, (250, 0), avatar)
        final_image.paste(base, (0, 0), base)

        b = BytesIO()
        final_image.save(b, format='png')
        b.seek(0)
        return send_file(body=b, content_type='image/png')


def setup():
    return Door()
