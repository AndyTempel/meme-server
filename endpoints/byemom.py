from io import BytesIO

from PIL import Image, ImageDraw, ImageFont
from aiohttp.web import Response as send_file

from utils import http
from utils.endpoint import Endpoint
from utils.imgutils import make_avatar
from utils.textutils import wrap


class Byemom(Endpoint):
    async def generate(self, request, avatars, text, usernames):
        base = Image.open('assets/byemom/mom.png')
        avatar = await make_avatar(
            Image.open(await http.get_image(request, avatars[0])).convert('RGBA').resize((250, 250), resample=Image.BICUBIC))
        avatar2 = avatar.copy().resize((125, 125), resample=Image.ANTIALIAS)
        avatar = avatar.resize((70, 70), Image.ANTIALIAS).rotate(-27, resample=Image.BICUBIC, expand=True)
        text_layer = Image.new('RGBA', (350, 25))
        bye_layer = Image.new('RGBA', (180, 51), (255, 255, 255))
        font = ImageFont.truetype(font='assets/fonts/arial.ttf', size=20)
        bye_font = ImageFont.truetype(font='assets/fonts/arimobold.ttf', size=14)
        canv = ImageDraw.Draw(text_layer)
        bye = ImageDraw.Draw(bye_layer)
        username = usernames[0] or 'tommy'
        msg = 'Alright {} I\'m leaving the house to run some errands'.format(username)

        text = wrap(font, text, 500)
        msg = wrap(font, msg, 200)

        canv.text((0, 0), text, font=font, fill='Black')
        bye.text((0, 0), msg, font=bye_font, fill=(42, 40, 165))
        text_layer = text_layer.rotate(24.75, resample=Image.BICUBIC, expand=True)

        base.paste(text_layer, (350, 443), text_layer)
        base.paste(bye_layer, (150, 7))
        base.paste(avatar, (513, 2), avatar)
        base.paste(avatar2, (70, 340), avatar2)

        b = BytesIO()
        base.save(b, format='png')
        b.seek(0)
        return send_file(body=b, content_type='image/png')


def setup():
    return Byemom()
