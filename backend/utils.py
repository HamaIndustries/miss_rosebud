import rosebud_configs

import os, random, requests
from PIL import Image

p_pink = 0xffd1dc


async def silentremove(filename):
    try:
        os.remove(filename)
    except OSError as e: 
        print('error removing {}'.format(filename))
        if e.errno != errno.ENOENT: 
            raise


async def send_image(image, cli, channel, tran = None):  # TODO: add lock to make this thread safe
    # with stuff_lock:
    try:
        if image.format == 'GIF':
            image.save('temp.gif', save_all=True, transparency=tran)
            await cli.send_file(channel, 'temp.gif')
            return
        bg = Image.new('RGBA', image.size)
        bg.paste(image, (0,0))
        bg.save('temp.png')
        await cli.send_file(channel, 'temp.png')
    except Exception as e:
        print('exception in send_image!')
        print('error: {}'.format(str(e)))
    finally:
        for i in ['temp.png', 'temp.gif']:
            if os.path.isfile(i):
                await silentremove(i)


def load_image_from_url(url):
    response = requests.get(url)
    return Image.open(BytesIO(response.content))


def gibberish():
    return random.choice('shxjxh  sjdjdj  sjdksjxj  shxjxhx  djdjdh  dhdjdhshd  dhdjdh  dhsjdh  dhdjd  ahdjshdh'.split())


def premultiply(im):
    pixels = im.load()
    for y in range(im.size[1]):
        for x in range(im.size[0]):
            r, g, b, a = pixels[x, y]
            if a != 255:
                r = r * a // 255
                g = g * a // 255
                b = b * a // 255
                pixels[x, y] = (r, g, b, a)


def unmultiply(im):
    pixels = im.load()
    for y in range(im.size[1]):
        for x in range(im.size[0]):
            r, g, b, a = pixels[x, y]
            if a != 255 and a != 0:
                r = 255 if r >= a else 255 * r // a
                g = 255 if g >= a else 255 * g // a
                b = 255 if b >= a else 255 * b // a
                pixels[x, y] = (r, g, b, a)


class TooSoonError(Exception):
    def __init__(self, current, goal):
        self.waittime = current - goal
