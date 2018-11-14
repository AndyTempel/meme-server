from io import BytesIO

from PIL import Image, ImageDraw, ImageFont
from aiohttp.web import Response as send_file

from utils.endpoint import Endpoint
from utils.textutils import auto_text_size


class Vr(Endpoint):
    async def generate(self, request, avatars, text, usernames):
        base = Image.open('assets/vr/vr.jpg').convert('RGBA')
        # We need a text layer here for the rotation
        font, text = await auto_text_size(text, ImageFont.truetype(font='assets/fonts/sans.ttf'), 207, font_scalar=0.8)
        canv = ImageDraw.Draw(base)
        w, h = canv.textsize(text)
        canv.multiline_text(((170-w), 485), text, font=font, fill='Black', anchor='center')

        b = BytesIO()
        base.save(b, format='png')
        b.seek(0)
        return send_file(body=b, content_type='image/png')


def setup():
    return Vr()
