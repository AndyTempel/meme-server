from io import BytesIO

from aiohttp.web import Response as send_file
from wand import image

from utils import http
from utils.endpoint import Endpoint


class Magik(Endpoint):
    async def generate(self, request, avatars, text, usernames):
        avatar = await http.get_image(request, avatars[0])
        with image.Image(file=avatar) as img:
            img.transform(resize='400x400')
            img.liquid_rescale(width=int(img.width * 0.5),
                               height=int(img.height * 0.5),
                               delta_x=0.5,
                               rigidity=0)
            img.liquid_rescale(width=int(img.width * 1.5),
                               height=int(img.height * 1.5),
                               delta_x=2,
                               rigidity=0)

            b = BytesIO()
            img.save(file=b)
            b.seek(0)
            return send_file(body=b, content_type='image/png')


def setup():
    return Magik()
