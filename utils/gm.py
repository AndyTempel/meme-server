import asyncio

from utils.http import get_image_raw


async def convert(request, image: str, args: list, output_format: str):
    img_bytes = await get_image_raw(request, image)
    args = ['gm', 'convert', '-'] + args + ['{}:-'.format(output_format)]

    proc = await asyncio.create_subprocess_exec(args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
                                                stdin=asyncio.subprocess.PIPE)
    stdout, stderr = await proc.communicate(img_bytes)
    return stdout
