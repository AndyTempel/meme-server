from io import BytesIO


async def get_image(request, url):
    async with request.app['client_session'].get(url) as response:
        if response.status != 200:
            raise Exception("Server returned an error: {}".format(response.status))
        f_handle = BytesIO()
        while True:
            chunk = await response.content.read(1024)
            if not chunk:
                break
            f_handle.write(chunk)
        await response.release()
        f_handle.seek(0)
        return f_handle


async def get_image_raw(request, url):
    async with request.app['client_session'].get(url) as response:
        if response.status != 200:
            raise Exception("Server returned an error: {}".format(response.status))
        out = await response.read()
        await response.release()
        return out

# def get_image(url):
#     return BytesIO(requests.get(url, stream=True).content)
#
#
# def get_image_raw(url):
#     return requests.get(url, stream=True).content
