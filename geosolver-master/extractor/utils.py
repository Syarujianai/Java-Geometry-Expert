import os
import tempfile
import re
import cv2
from collections import namedtuple


def display_image(image, title="", block=True):
    cv2.imshow(title, image)
    if block:
        cv2.waitKey()
        cv2.destroyAllWindows()


instantiator_defs = {
    'point': (('x', 'number'), ('y', 'number')),
    'line': (('a', 'point'), ('b', 'point')),
    'angle': (('a', 'point'), ('b', 'point'), ('c', 'point')),
    'circle': (('center', 'point'), ('radius', 'number')),
    'arc': (('circle', 'circle'), ('a', 'point'), ('b', 'point')),
    'triangle': (('a', 'point'), ('b', 'point'), ('c', 'point')),
    'quad': (('a', 'point'), ('b', 'point'), ('c', 'point'), ('d', 'point')),
    'hexagon': (('a', 'point'), ('b', 'point'), ('c', 'point'), ('d', 'point'), ('e', 'point'), ('f', 'point')),
    'para': (('a', 'point'), ('b', 'point'), ('c', 'point'), ('d', 'point')),
    'rectangle': (('a', 'point'), ('b', 'point'), ('c', 'point'), ('d', 'point')),
    'trapezoid': (('a', 'point'), ('b', 'point'), ('c', 'point'), ('d', 'point')),
    'rhombus': (('a', 'point'), ('b', 'point'), ('c', 'point'), ('d', 'point')),
    'square': (('a', 'point'), ('b', 'point'), ('c', 'point'), ('d', 'point')),
}

instantiators = {}
# instantiators['polygon'] = polygon
for key, value in instantiator_defs.iteritems():
    args, _ = zip(*value)
    nt = namedtuple(key, ' '.join(args))
    instantiators[key] = nt
