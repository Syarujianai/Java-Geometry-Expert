from geosolver.diagram.parse_image_segments import parse_image_segments
from geosolver.diagram.parse_primitives import parse_primitives
from geosolver.diagram.select_primitives import select_primitives
from geosolver.diagram.parse_core import parse_core
from geosolver.diagram.parse_graph import parse_graph
from geosolver.diagram.get_instances import get_all_instances

from geosolver.utils import prep
from geosolver.diagram.draw_on_image import *
import cv2
import os
import pickle
from geosolver.diagram.my_segments import Geometry_Extractor
from timeout import  timeout
from multiprocessing import Pool

@timeout(40)
def extract(image, i):
    # print('----a')
    image_segment_parse, detected_char = ge.parse_image_segments(image)
    primitive_parse = parse_primitives(image_segment_parse)
    selected = select_primitives(primitive_parse)
    core_parse = parse_core(selected)
    # print('----p')
    graph_parse = parse_graph(core_parse)
    # print('----g')
    pairs = []
    points = get_all_instances(graph_parse, 'point')
    # print('----1')
    lines = get_all_instances(graph_parse, 'line')
    # print('----2')
    circles = get_all_instances(graph_parse, 'circle')
    # print('----3')
    angles = get_all_instances(graph_parse, 'angle')
    # print('----4')
    polygon = get_all_instances(graph_parse, 'polygon')
    # pr0int('----5')
    for point in points.keys():
        points[point] = (points[point].x, points[point].y)

    image = core_parse.get_image_points()
    for line in lines.values():
        image = draw_line2(image, line, offset=image_segment_parse.diagram_image_segment.offset)
    # cv2.imwrite('tmp/results/im_lines.png', image)
    # image = cv2.imread(image_path)
    for circle in circles.values():
        image = draw_circle2(image, circle, offset=image_segment_parse.diagram_image_segment.offset)
    cv2.imwrite('tmp/results/{}entity.png'.format(i), image)
    return { 'id':i,
            'points': points,
            'lines': lines.keys(),
            'circles': circles.keys(),
            'angles': angles.keys(),
            'polygon': polygon.keys(),
            'chars': detected_char}

def fuck(i):
    try:
        image = cv2.imread(image_path.format(i), cv2.IMREAD_GRAYSCALE)
        extracted = extract(image, i)
        print(i, 'ok')
        return extracted
    except:
        print(i, 'NO')
        return {}

image_path = 'tmp/images2/{}.png'
result_path = 'tmp/all_results/'
# rescale to 256*256
error_images = []

ge = Geometry_Extractor()
# for i, image_name in enumerate(os.listdir(image_path)[:100]):

# for i in range(4999, 5000):   # len(os.listdir('tmp/all_images/')))
#     try:
#         image = cv2.imread(image_path.format(i), cv2.IMREAD_GRAYSCALE)
#         extract_list.append(extract(image, i))
#         print(i, 'ok')
#     except:
#         extract_list.append({})
#         print(i, 'NO')
# p = Pool(processes=18)
# extract_list = p.map(fuck, range(9939))
# p.terminate()


# print(extract_list)
with open('extracted_417_2.pk', 'rb') as f:
    extract_list = pickle.load(f)

print(len(extract_list))

for sample in extract_list:
    pairs = []
    for char in sample['chars'].keys():
        top_left, bottom_right = sample['chars'][char]
        mid_point = ((top_left[0] + bottom_right[0]) / 2, (top_left[1] + bottom_right[1]) / 2)
        for pointid, loc in sample['point'].items():
            distance = (mid_point[0] - loc[0]) ** 2 + (mid_point[1] - loc[1]) ** 2
            pairs.append((distance, char, pointid))


# with open('extracted_416_1.pk', 'rb') as f:
#     extract_list1 = pickle.load(f)
#
# with open('extracted_416_2.pk', 'rb') as f:
#     extract_list2 = pickle.load(f)
#
# extract_lists = extract_list1 + extract_list + extract_list2

# with open('extracted_417.pk', 'rb') as f:
#     extract_list = pickle.load(f)
#
#
# print(extract_list[0])