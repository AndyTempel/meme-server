from io import BytesIO

from PIL import Image, ImageDraw, ImageFont
from aiohttp.web import Response as send_file

from utils.endpoint import Endpoint
from utils.textutils import auto_text_size


class Balloon(Endpoint):
    async def generate(self, request, avatars, text, usernames):
        base = Image.open('assets/balloon/balloon.jpg').convert('RGBA')
        font = ImageFont.truetype(font='assets/fonts/sans.ttf')
        canv = ImageDraw.Draw(base)

        text = text.split(', ')

        if len(text) != 2:
            text = ["Separate the items with a", "comma followed by a space"]

        balloon, label = text

        balloon_text_1_font, balloon_text_1 = await auto_text_size(balloon, font, 162)
        balloon_text_2_font, balloon_text_2 = await auto_text_size(balloon, font, 170, font_scalar=0.95)
        balloon_text_3_font, balloon_text_3 = await auto_text_size(balloon, font, 110, font_scalar=0.8)
        label_font, label_text = await auto_text_size(label, font, 125)

        canv.text((80, 180), balloon_text_1, font=balloon_text_1_font, fill='Black')
        canv.text((50, 530), balloon_text_2, font=balloon_text_2_font, fill='Black')
        canv.text((500, 520), balloon_text_3, font=balloon_text_3_font, fill='Black')
        canv.text((620, 155), label_text, font=label_font, fill='Black')

        b = BytesIO()
        base.save(b, format='png')
        b.seek(0)
        return send_file(body=b, content_type='image/png')


def setup():
    return Balloon()
