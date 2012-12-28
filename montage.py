#!/bin/env python
import math
import glob
import subprocess
import itertools
import os
import fnmatch

matches = []
def filegenerator():
    for root, dirnames, filenames in os.walk('.'):
        for filename in fnmatch.filter(filenames, '*.jpg'):
            yield os.path.join(root, filename)

ifiles = filegenerator()

TILE_SIZE = 76
IMAGE_SIZE = 64 #num avatars wide

def get_image(size, level, x, y):
    if not os.path.exists('%s/%d' % ("avatar_files", level)):
        os.mkdir('%s/%d' % ("avatar_files", level))
    outfile = 'avatar_files/%s/%s_%s.jpg' % (level, x, y)
    if size == 1:
        os.link(ifiles.next(), outfile)
        return outfile
    if level >= 8:
        subprocess.call(['gm', 'montage', '-tile', '2x2', '-geometry', '%dx%d' % (TILE_SIZE/2, TILE_SIZE/2),
                         get_image(size/2, level+1, x*2, y*2),
                         get_image(size/2, level+1, x*2+1, y*2),
                         get_image(size/2, level+1, x*2, y*2+1),
                         get_image(size/2, level+1, x*2+1, y*2+1),
                         outfile])
    else:
        srcfile = get_image(size, level+1, 0, 0)
        s = '%dx%d' % (2**level, 2**level)
        subprocess.call(['gm', 'convert', '-size', s, srcfile, '-resize', s, outfile])
    return outfile

get_image(IMAGE_SIZE, 0, 0, 0)
with open('avatar.dzi', 'w') as f:
    x = IMAGE_SIZE*TILE_SIZE*2
    f.write('<?xml version="1.0" encoding="UTF-8"?><Image TileSize="%d" Overlap="0" Format="jpg" xmlns="http://schemas.microsoft.com/deepzoom/2008"><Size Width="%s" Height="%s"/></Image>' % (TILE_SIZE*2, x, x))
