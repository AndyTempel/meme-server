from io import BytesIO

from PIL import Image, ImageDraw
from aiohttp.web import Response as send_file

from utils.endpoint import Endpoint
from utils.textutils import auto_text_size


class Boo(Endpoint):
    async def generate(self, request, avatars, text, usernames):
        base = Image.open('assets/boo/boo.png').convert('RGBA')
        # We need a text layer here for the rotation
        canv = ImageDraw.Draw(base)

        text = text.split(', ')

        if len(text) != 2:
            text = ["Separate the items with a", "comma followed by a space"]

        first, second = text

        first_font, first_text = await auto_text_size(first, ImageFont.truetype(font='assets/fonts/sans.ttf'), 144,
                                                font_scalar=0.7)
        second_font, second_text = await auto_text_size(second, ImageFont.truetype(font='assets/fonts/sans.ttf'), 144,
                                                  font_scalar=0.7)

        canv.text((35, 54), first_text, font=first_font, fill='Black')
        canv.text((267, 57), second_text, font=second_font, fill='Black')

        b = BytesIO()
        base.save(b, format='png')
        b.seek(0)
        return send_file(body=b, content_type='image/png')


def setup():
    return Boo()
