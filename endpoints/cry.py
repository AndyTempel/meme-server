from io import BytesIO

from aiohttp.web import Response as send_file
from PIL import Image, ImageDraw, ImageFont

from utils.endpoint import Endpoint
from utils.textutils import wrap


class Cry(Endpoint):
    async def generate(self, request, avatars, text, usernames):
        base = Image.open('assets/cry/cry.jpg')
        font = ImageFont.truetype(font='assets/fonts/tahoma.ttf', size=20)
        canv = ImageDraw.Draw(base)

        text = wrap(font, text, 180)
        canv.text((382, 80), text, font=font, fill='Black')

        b = BytesIO()
        base.save(b, format='png')
        b.seek(0)
        return send_file(body=b, content_type='image/png')


def setup():
    return Cry()
