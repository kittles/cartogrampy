import random
import itertools as itr
from PIL import Image, ImageDraw
import numpy as np
import colored_traceback
import subprocess as sp
colored_traceback.add_hook()

def prod (xs, ys, margin=0):
    return itr.product(range(xs - margin), range(ys - margin))

def generate_control_points (w, h, w_cnt, h_cnt):
    # generates a grid of control points
    cps = np.zeros((h_cnt, w_cnt, 2))
    xs = np.linspace(0, w, w_cnt)
    ys = np.linspace(0, h, h_cnt)
    for x, y in prod(w_cnt, h_cnt):
        cps[y,x] = np.array([xs[x], ys[y]])
    return cps

def cp_rect (x, y, cps):
    # get a rect from a specific control point
    # uses the control point down and to the right of it
    top_left = cps[y,x]
    bottom_right = cps[y+1,x+1] # should handle error
    return (
        int(top_left[0]),
        int(top_left[1]),
        int(bottom_right[0]),
        int(bottom_right[1]),
    )

def cp_quad (x, y, cps):
    # a quadrilateral built from the south, south east, and east neighbors
    # this is the format PIL expects for mesh
    points = (
        cps[y,x],
        cps[y+1,x],
        cps[y+1,x+1],
        cps[y,x+1],
    )
    return tuple([int(i) for point in points for i in point])

def displace_point (x, y, vec, mesh):
    mesh[y,x] += vec
    return mesh[y,x]

################################################################################

for i in range(1,100):
    print(i)
    w, h = 498, 498

    # test image
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


    # actual image
    #im = Image.open('total_2015_498x498.png')


    # fake data
    z = np.zeros((w, h))
    z += 10
    z[300:400,100:200] += i

    # real data
    #z = np.array(Image.open('total_2015_498x498.png').convert('L'))
    #z += 50

    # write z to file
    with open('data/z.dat', 'w') as fh:
        for row in z:
            fh.write(' '.join([str(i) for i in row]) + '\n')

    # generate displacement data
    cmd = 'cart {} {} data/z.dat data/disp.dat'.format(w, h)
    sp.run(cmd, shell=True)

    with open('data/points', 'w') as fh:
        for x,y in itr.product(np.linspace(0,w-1,w), np.linspace(0,h-1,h)):
            fh.write('{} {}\n'.format(x, y))

    cmd = 'cat data/points | interp {} {} data/disp.dat > data/points_disp'.format(w, h)
    sp.run(cmd, shell=True)

    # use data to displace
    w_cnt, h_cnt = w, h
    control_points = generate_control_points(w, h, w_cnt, h_cnt)
    deformed_points = control_points.copy()

    pts = open('data/points', 'r')
    pts_dsp = open('data/points_disp', 'r')

    for pt, pt_dsp in zip(pts, pts_dsp):
        x, y = [float(i) for i in pt.split(' ')]
        xd, yd = [float(i) for i in pt_dsp.split(' ')]
        dsp_vec = np.array([x - xd, y - yd])
        displace_point(int(x), int(y), dsp_vec, deformed_points)

    #for x, y in xys_itr(w_cnt, h_cnt):
    #    p = control_points[y,x].copy()
    #    p[0] += int(random.random() * 50)
    #    p[1] += int(random.random() * 50)
    #    deformed_points[y,x] = p

    transforms = []
    for x, y in prod(w_cnt, h_cnt, 1):
        transforms.append((
            cp_rect(x, y, control_points),
            cp_quad(x, y, deformed_points)
        ))


    ## show initial control points
    #d = ImageDraw.Draw(im)
    #for p in itr.product(np.linspace(0,1024,512), np.linspace(0,512,256)):
    #    r_val = int(255 * (p[0] / 498))
    #    g_val = int(255 * (p[1] / 498))
    #    b_val = 255 - int(255 * (p[1] / 498))
    #    d.point(p, fill=(r_val,g_val,b_val))

    # apply transforms
    im = im.transform(im.size, Image.MESH, transforms, Image.BILINEAR)

    # show deformed control points
    d = ImageDraw.Draw(im)
    d.line([(100,300), (100,400), (200,400), (200,300), (100,300)], fill=(255,0,0))
    im.save('output/{:03}.png'.format(i))
