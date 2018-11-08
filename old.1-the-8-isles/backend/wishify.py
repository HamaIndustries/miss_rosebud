from blend_modes import blend_modes
from PIL import Image
import os
import numpy

def screen(im, app, opacity):
    im_arr = numpy.array(im)
    im_arrfloat = im_arr.astype(float)
    app_arr = numpy.array(app)
    app_arrfloat = app_arr.astype(float)
    out = blend_modes.screen(im_arrfloat, app_arrfloat, opacity)
    out = Image.fromarray(numpy.uint8(out))
    return out

def colorify(inpu, hex='ffd1dc', opacity=1):
    im = inpu.convert('RGBA')
    app = Image.new('RGBA', im.size, tuple(int(hex[i:i+2], 16) for i in (0, 2 ,4)))
    return screen(im, app, opacity)

#colorify(Image.open('68.png')).show()
