from io import BytesIO

from aiohttp.web import Response as send_file
from PIL import Image

from utils import http
from utils.endpoint import Endpoint


class Screams(Endpoint):
    async def generate(self, request, avatars, text, usernames):
        base = Image.open('assets/screams/screams.jpg').convert('RGBA')
        avatar = Image.open(await http.get_image(request, avatars[0])).resize((175, 175)).convert('RGBA')
        avatar2 = Image.open(await http.get_image(request, avatars[1])).resize((156, 156)).convert('RGBA')
        base.paste(avatar, (200, 1), avatar)
        base.paste(avatar2, (136, 231), avatar2)

        b = BytesIO()
        base.save(b, format='png')
        b.seek(0)
        return send_file(body=b, content_type='image/png')


def setup():
    return Screams()
