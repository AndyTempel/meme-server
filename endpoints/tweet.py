from io import BytesIO

from aiohttp.web import Response as send_file
from PIL import Image, ImageDraw, ImageFont

from utils.endpoint import Endpoint
from utils.textutils import wrap


class Tweet(Endpoint):
    async def generate(self, request, avatars, text, usernames):
        base = Image.open('assets/tweet/trump.jpg')
        font = ImageFont.truetype(font='assets/fonts/segoeuireg.ttf', size=50)
        canv = ImageDraw.Draw(base)
        text = wrap(font, text, 1150)
        canv.text((45, 160), text, font=font, fill='Black')

        b = BytesIO()
        base.save(b, format='png')
        b.seek(0)
        return send_file(body=b, content_type='image/png')


def setup():
    return Tweet()
