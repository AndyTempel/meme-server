from io import BytesIO

from PIL import Image, ImageDraw
from aiohttp.web import Response as send_file

from utils.endpoint import Endpoint
from utils.textutils import auto_text_size


class Armor(Endpoint):
    async def generate(self, request, avatars, text, usernames):
        base = Image.open('assets/armor/armor.png').convert('RGBA')
        # We need a text layer here for the rotation
        font, text = await auto_text_size(text, ImageFont.truetype(font='assets/fonts/comic.ttf'), 207, font_scalar=1.5)
        canv = ImageDraw.Draw(base)

        canv.text((34, 355), text, font=font, fill='Black')

        b = BytesIO()
        base.save(b, format='png')
        b.seek(0)
        return send_file(body=b, content_type='image/png')


def setup():
    return Armor()
