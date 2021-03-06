from io import BytesIO

from aiohttp.web import Response as send_file
from PIL import Image

from utils import http
from utils.endpoint import Endpoint


class Bed(Endpoint):
    async def generate(self, request, avatars, text, usernames):
        base = Image.open('assets/bed/bed.png').convert('RGBA')
        avatar = Image.open(await http.get_image(request, avatars[0])).resize((100, 100)).convert('RGBA')
        avatar2 = Image.open(await http.get_image(request, avatars[1])).resize((70, 70)).convert('RGBA')
        avatar_small = avatar.copy().resize((70, 70))
        base.paste(avatar, (25, 100), avatar)
        base.paste(avatar, (25, 300), avatar)
        base.paste(avatar_small, (53, 450), avatar_small)
        base.paste(avatar2, (53, 575), avatar2)

        b = BytesIO()
        base.save(b, format='png')
        b.seek(0)
        return send_file(body=b, content_type='image/png')


def setup():
    return Bed()
