from collections import namedtuple
import numpy as np

__author__ = 'minjoon'

"""
eps is used to segment the line.
It shouldn't be too big; otherwise, off-line will be matched.
"""
HoughLineParameters = namedtuple("HoughLineParameters",
                                 "rho theta threshold max_gap min_length nms_rho nms_theta max_num eps")

hough_line_parameters = HoughLineParameters(rho=1,
                                            theta=np.pi/180,
                                            threshold=30,
                                            max_gap=3,
                                            min_length=20,
                                            nms_rho=2,
                                            nms_theta=np.pi/60,
                                            max_num=30,
                                            eps=2)

HoughCircleParameters = namedtuple("HoughCircleParameters",
                                   "dp minRadius maxRadius param1 param2 minDist max_gap min_length max_num")

hough_circle_parameters = HoughCircleParameters(dp=1,
                                                minRadius=20,
                                                maxRadius=100,
                                                param1=50,
                                                param2=30,
                                                minDist=2,
                                                max_gap=100,
                                                min_length=20,
                                                max_num=20)

# These eps determine pixel coverage of each primitive.
LINE_EPS = 7
CIRCLE_EPS = 3
PRIMITIVE_SELECTION_MIN_GAIN = 10

INTERSECTION_EPS = 3
KMEANS_RADIUS_THRESHOLD = 6

MAX_POINTS = 10
