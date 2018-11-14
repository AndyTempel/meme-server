from io import BytesIO

from PIL import Image, ImageDraw, ImageFont
from aiohttp.web import Response as send_file

from utils.endpoint import Endpoint
from utils.textutils import wrap


class Ohno(Endpoint):
    async def generate(self, request, avatars, text, usernames):
        base = Image.open('assets/ohno/ohno.png').convert('RGBA')
        font = ImageFont.truetype(font='assets/fonts/sans.ttf', size=16 if len(text) > 38 else 32)
        canv = ImageDraw.Draw(base)

        text = wrap(font, text, 260)
        canv.text((340, 30), text, font=font, fill='Black')

        b = BytesIO()
        base.save(b, format='png')
        b.seek(0)
        return send_file(body=b, content_type='image/png')


def setup():
    return Ohno()
