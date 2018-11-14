import random


async def modify_all_pixels(im, noise_gen):
    width, height = im.size
    pxls = im.load()
    for x in range(width):
        for y in range(height):
            pxls[x, y] = await noise_gen(x, y, *pxls[x, y])


async def add_noise(image, strength=100):
    async def pixel_noise(x, y, r, g, b):
        noise = int(random.randint(0, strength) - strength / 2)
        return max(0, min(r + noise, 255)), max(0, min(g + noise, 255)), max(0, min(b + noise, 255))
    await modify_all_pixels(image, pixel_noise)
    return image
