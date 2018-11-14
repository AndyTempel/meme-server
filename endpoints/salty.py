from io import BytesIO
from random import randint

from PIL import Image
from aiohttp.web import Response as send_file

from utils import http
from utils.endpoint import Endpoint


class Salty(Endpoint):
    async def generate(self, request, avatars, text, usernames):
        avatar = Image.open(await http.get_image(request, avatars[0])).convert('RGBA').resize((256, 256))

        salt = (
            Image.open('assets/salty/salt.png')
            .convert('RGBA')
            .resize((256, 256))
            .rotate(-130, resample=Image.BICUBIC)
        )

        blank = Image.new('RGBA', (256, 256))
        blank.paste(avatar, (0, 0), avatar)
        frames = []

        for i in range(8):
            base = blank.copy()
            if i == 0:
                base.paste(salt, (-125, -125), salt)
            else:
                base.paste(salt, (-135 + randint(-5, 5), -135 + randint(-5, 5)), salt)

            frames.append(base)

        b = BytesIO()
        frames[0].save(b, save_all=True, append_images=frames[1:], format='gif', loop=0, duration=20,
                       optimize=True)
        b.seek(0)
        return send_file(body=b, content_type='image/gif')


def setup():
    return Salty()
