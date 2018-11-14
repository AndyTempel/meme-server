from io import BytesIO

from aiohttp.web import Response as send_file
from PIL import Image

from utils import http
from utils.endpoint import Endpoint


class Slap(Endpoint):
    async def generate(self, request, avatars, text, usernames):
        base = Image.open('assets/batslap/batslap.jpg').resize((1000, 500)).convert('RGBA')
        avatar = Image.open(await http.get_image(request, avatars[1])).resize((220, 220)).convert('RGBA')
        avatar2 = Image.open(await http.get_image(request, avatars[0])).resize((200, 200)).convert('RGBA')
        base.paste(avatar, (580, 260), avatar)
        base.paste(avatar2, (350, 70), avatar2)

        b = BytesIO()
        base.save(b, format='png')
        b.seek(0)
        return send_file(body=b, content_type='image/png')


def setup():
    return Slap()
