from io import BytesIO

from aiohttp.web import Response as send_file
from PIL import Image, ImageDraw, ImageFont

from utils.endpoint import Endpoint
from utils.textutils import wrap


class Shit(Endpoint):
    async def generate(self, request, avatars, text, usernames):
        base = Image.open('assets/shit/shit.jpg')
        font = ImageFont.truetype(font='assets/fonts/segoeuireg.ttf', size=30)

        # We need a text layer here for the rotation
        text_layer = Image.new('RGBA', base.size)
        canv = ImageDraw.Draw(text_layer)

        text = wrap(font, text, 350)
        canv.text((0, 570), text, font=font, fill='Black')
        text_layer = text_layer.rotate(52, resample=Image.BICUBIC)

        base.paste(text_layer, (0, 50), text_layer)

        b = BytesIO()
        base.save(b, format='png')
        b.seek(0)
        return send_file(body=b, content_type='image/png')


def setup():
    return Shit()
