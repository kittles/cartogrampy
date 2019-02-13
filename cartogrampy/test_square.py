import math
import itertools as itr
import numpy as np
from PIL import Image, ImageDraw
from generate import *

for step in range(26,50):
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

    z = np.zeros((w, h))
    z += 5

    squares = [
        [100,100,200,200],
        [250,250,400,400],
        [100,400,200,500],
    ]

    for square in squares:
        x1, y1, x2, y2 = square
        d.line([(x1,y1), (x1,y2), (x2,y2), (x2,y1), (x1,y1)], fill=(0,255,0))
        z[y1:y2,x1:x2] += step

    d.ellipse((350, 100, 450, 200), outline=(0,255,0))
    # find points within circle centered at 400, 150 with radius 50
    for x,y in itr.product(range(w), range(h)):
        if math.sqrt((x - 400)**2 + (y - 150)**2) <= 50:
            z[y,x] += step * 1.5

    im = cartogram(im, z)
    im.save('tmp/{:03}.png'.format(step))
