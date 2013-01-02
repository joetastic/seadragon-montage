#!/bin/env python
import math
import glob
import subprocess
import itertools
import os
import fnmatch

def filegenerator():
    for root, dirnames, filenames in os.walk('originals'):
        for filename in fnmatch.filter(filenames, '*.jpg'):
            yield os.path.join(root, filename)

#ifiles = filegenerator()
filereader = open('images.rand','r')

IMAGE_TILE = 9
TILE_SIZE = 76*IMAGE_TILE
IMAGE_SIZE = IMAGE_TILE*(2**7) #num avatars wide

def next_image():
    try:
        #return ifiles.next()
        return filereader.readline().strip()
    except StopIteration, e:
        return 'NULL:'

SINGLE_IMAGE = math.ceil(math.log(TILE_SIZE,2))

level14_counter = 0

def get_image(size, level, x, y):
    global level14_counter
    if not os.path.exists('%s/%d' % ("avatar_files", level)):
        os.mkdir('%s/%d' % ("avatar_files", level))
    outfile = 'avatar_files/%s/%s_%s.jpg' % (level, x, y)
    if size == IMAGE_TILE:
        subprocess.call(['gm', 'montage',
                         '-tile', '%dx%d' % (IMAGE_TILE, IMAGE_TILE),
                         '-background', 'black',
                         '-bordercolor', 'black',
                         '-borderwidth', '1',
                         '-geometry','76x76'] +
                        [next_image() for x in xrange(0, IMAGE_TILE**2)] +
                        [outfile])
        return outfile
    elif size < IMAGE_TILE:
        raise Exception('no good, bad size %f' % size)
    if level == SINGLE_IMAGE:
        subprocess.call(['gm', 'montage',
                         '-tile', '2x1',
                         '-geometry', '%dx%d' % (TILE_SIZE/2, TILE_SIZE/2),
                         get_image(size/2, level+1, x*2, y*2),
                         get_image(size/2, level+1, x*2+1, y*2),
                         outfile])
    elif level > SINGLE_IMAGE:
        subprocess.call(['gm', 'montage',
                         '-tile', '2x2',
                         '-geometry', '%dx%d' % (TILE_SIZE/2, TILE_SIZE/2),
                         get_image(size/2, level+1, x*2, y*2),
                         get_image(size/2, level+1, x*2+1, y*2),
                         get_image(size/2, level+1, x*2, y*2+1),
                         get_image(size/2, level+1, x*2+1, y*2+1),
                         outfile])
    else:
        srcfile = get_image(size, level+1, 0, 0)
        if level == 0:
            s = '1x1'
        else:
            s = '%dx%d' % (2**level, 2**(level-1))
        subprocess.call(['gm', 'convert', '-size', s, srcfile, '-resize', s, outfile])
    if level == 14:
        level14_counter += 1
        print "\033[1F\033[1G%d/128" % level14_counter
    return outfile

print '0/128'
get_image(IMAGE_SIZE, 0, 0, 0)

filereader.close()

with open('avatar.dzi', 'w') as f:
    x = IMAGE_SIZE*TILE_SIZE/IMAGE_TILE
    f.write('<?xml version="1.0" encoding="UTF-8"?>'
            '<Image TileSize="%d" Overlap="0" Format="jpg" '
                   'xmlns="http://schemas.microsoft.com/deepzoom/2008">'
            '<Size Width="%s" Height="%s"/></Image>' % (TILE_SIZE, x, x/2))
