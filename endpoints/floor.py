from io import BytesIO

from PIL import Image, ImageDraw, ImageFont
from aiohttp.web import Response as send_file

from utils import http
from utils.endpoint import Endpoint
from utils.textutils import wrap


class Floor(Endpoint):
    async def generate(self, request, avatars, text, usernames):
        base = Image.open('assets/floor/floor.jpg').convert('RGBA')
        avatar = Image.open(await http.get_image(request, avatars[0])).resize((45, 45)).convert('RGBA')
        avatar2 = avatar.copy().resize((23, 23))
        font = ImageFont.truetype(font='assets/fonts/sans.ttf', size=22)
        canv = ImageDraw.Draw(base)

        text = wrap(font, text, 300)
        canv.text((168, 36), text, font=font, fill='Black')

        base.paste(avatar, (100, 90), avatar)
        base.paste(avatar2, (330, 90), avatar2)

        b = BytesIO()
        base.save(b, format='png')
        b.seek(0)
        return send_file(body=b, content_type='image/png')


def setup():
    return Floor()
