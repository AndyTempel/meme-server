from PIL import Image, ImageDraw, ImageOps


async def make_avatar_mask(avatar):
    poly = Image.new('RGBA', avatar.size)
    pdraw = ImageDraw.Draw(poly)
    pdraw.ellipse([(0, 0), *avatar.size], fill=(255, 255, 255, 255))

    if poly.mode == 'RGBA':
        r, g, b, a = poly.split()
        rgb_image = Image.merge('RGB', (r, g, b))
        inverted = ImageOps.invert(rgb_image)
        r, g, b = inverted.split()
        iv = Image.merge('RGBA', (r, g, b, a))
    else:
        iv = ImageOps.invert(poly)

    return iv


async def make_avatar(avatar):
    print(avatar.size)
    base = Image.new("RGBA", avatar.size)
    mask = await make_avatar_mask(avatar.copy())
    base.paste(avatar, (0, 0), mask=mask)
    return base
