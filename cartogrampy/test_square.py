import itertools as itr
import numpy as np
from PIL import Image, ImageDraw
from generate import cartogram

w, h = 500, 500
im = Image.fromarray(np.zeros((w, h)), 'RGB')
d = ImageDraw.Draw(im)
xs = np.linspace(0, w, int(w / 2))
ys = np.linspace(0, h, int(h / 2))
for p in itr.product(xs, ys):
    r_val = int(255 * (p[0] / 498))
    g_val = int(255 * (p[1] / 498))
    b_val = 255 - int(255 * (p[1] / 498))
    d.point(p, fill=(r_val,g_val,b_val))
d.line([(100,300), (100,400), (200,400), (200,300), (100,300)], fill=(0,255,0))

z = np.zeros((w, h))
z += 10
z[300:400,100:200] += 20

im = cartogram(im, z)
im.show()


# show deformed control points
#d = ImageDraw.Draw(im)
#d.line([(100,300), (100,400), (200,400), (200,300), (100,300)], fill=(255,0,0))
#im.save('output/{:03}.png'.format(i))
