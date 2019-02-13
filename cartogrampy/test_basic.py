import numpy as np
from PIL import Image, ImageDraw
import generate

# the image that you will distort into a cartogram
#im = Image.open('path/to/image.png')
# for simple test, just use numpy array
w,h = 500,500
im = Image.fromarray(np.zeros((w,h)), mode='RGB')
d = ImageDraw.Draw(im)

# the data that will determine the distortion- if you were doing population, say, the points of this 2d array would be
# the population of whichever region that point falls in.
z = np.zeros((w, h)) # or whatever
z += 1 # add a baseline... this seems to help cartograms from distorting
# as an example, add some square regions with higher "density"
squares = [
    [100,100,200,200],
    [250,250,400,400],
    [100,400,200,450],
]
for square in squares:
    x1, y1, x2, y2 = square
    # draw boxes in green. these will get distorted by the transformation
    d.line([(x1,y1), (x1,y2), (x2,y2), (x2,y1), (x1,y1)], fill=(0,255,0)) # outline them
    z[y1:y2,x1:x2] += 3 # density is 4 times the baseline of 1
im = generate.cartogram(im, z)
d = ImageDraw.Draw(im)
# show initial boxes in red for referrence
for square in squares:
    x1, y1, x2, y2 = square
    d.line([(x1,y1), (x1,y2), (x2,y2), (x2,y1), (x1,y1)], fill=(255,0,0))
im.show()
