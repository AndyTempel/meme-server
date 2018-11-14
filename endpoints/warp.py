from io import BytesIO
from random import choice, randint

from aiohttp.web import Response as send_file

from utils import gm
from utils.endpoint import Endpoint


class Warp(Endpoint):
    async def generate(self, request, avatars, text, usernames):
        implode = '-{}'.format(str(randint(3, 15)))
        roll = '+{}+{}'.format(randint(0, 256), randint(0, 256))
        swirl = '{}{}'.format(choice(["+", "-"]), randint(120, 180))
        concat = ['-implode', implode, '-roll', roll, '-swirl', swirl]

        output = await gm.convert(request, avatars[0], concat, 'png')

        b = BytesIO(output)
        b.seek(0)
        return send_file(body=b, content_type='image/png')


def setup():
    return Warp()
