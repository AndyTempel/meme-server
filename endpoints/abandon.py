from io import BytesIO
from utils.textutils import wrap

from aiohttp.web import Response as send_file
from PIL import Image, ImageDraw, ImageFont

from utils.endpoint import Endpoint


class Abandon(Endpoint):
    async def generate(self, request, avatars, text, usernames):
        base = Image.open('assets/abandon/abandon.png')
        font = ImageFont.truetype(font='assets/fonts/verdana.ttf', size=24)
        canv = ImageDraw.Draw(base)
        text = wrap(font, text, 320)
        canv.text((25, 413), text, font=font, fill='Black')

        b = BytesIO()
        base.save(b, format='png')
        b.seek(0)
        return send_file(body=b, content_type='image/png')


def setup():
    return Abandon()
