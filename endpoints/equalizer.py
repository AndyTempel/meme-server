from io import BytesIO

from PIL import Image
from aiohttp.web import Response as send_file

from utils.endpoint import Endpoint

SLIDER_POINTS = [77, 119, 161, 203, 244, 286, 328, 369, 411, 453, 495, 536, 578, 620, 662]
ZERO_GAIN_POSITION = 352
MAX_GAIN_POSITION = (46, 306)
MIN_GAIN_POSITION = (428, 76)


class Equalizer(Endpoint):
    async def generate(self, request, avatars, text, usernames):
        base = Image.open('assets/equalizer/equalizer-with-title.png').convert('RGBA')
        slider = Image.open('assets/equalizer/slider.png').convert('RGBA')
        slider_select = Image.open('assets/equalizer/slider-selected.png').convert('RGBA')
        try:
            selected_slider = int(avatars[0]) if avatars[0] else -1
        except ValueError:
            selected_slider = -1

        equalizer = [0.0 for x in range(15)]
        for i, val in enumerate(text.split(",")):
            equalizer[i] = val

        # Put the sliders on the blank eq
        for x in range(15):
            try:
                gain = max(min(float(equalizer[x]), 1.0), -0.25)
            except ValueError:
                gain = 0.0
            if gain == 0.0:
                height = ZERO_GAIN_POSITION
            elif gain < 0.0:
                height = int((abs(gain * 4) * MIN_GAIN_POSITION[1]) + ZERO_GAIN_POSITION)
            else:
                height = int(ZERO_GAIN_POSITION - (gain * MAX_GAIN_POSITION[1]))
            if x == selected_slider:
                base.paste(slider_select, (SLIDER_POINTS[x] - 12, height), slider_select)
            else:
                base.paste(slider, (SLIDER_POINTS[x] - 12, height), slider)

        b = BytesIO()
        base.save(b, format='png')
        b.seek(0)
        return send_file(body=b, content_type='image/png')


def setup():
    return Equalizer()
