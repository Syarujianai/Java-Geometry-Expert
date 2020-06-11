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

image_path = 'tmp/all_images/{}.png'
result_path = 'tmp/all_results/'
# rescale to 256*256
error_images = []

ge = Geometry_Extractor()
# for i, image_name in enumerate(os.listdir(image_path)[:100]):
extract_list = []

for i in range(len(os.listdir('tmp/all_images/'))):   # len(os.listdir('tmp/all_images/')))
    if i % 1 == 0:
        print(i)
    match_char = {}
    try:
        image = cv2.imread(image_path.format(i), cv2.IMREAD_GRAYSCALE)
        # if(image.sum()) == 0:
        #     image = cv2.imread(image_path + image_path.format(i), -1)
        #     image = image[:, :, 3]
        #     maxd = image.max()
        #     mind = image.min()
        #     image = (1 - (image - mind) / (maxd - mind)) * 255
        #     image = image.astype(np.uint8)
        image_segment_parse, detected_char = ge.parse_image_segments(image)
        primitive_parse = parse_primitives(image_segment_parse)
        selected = select_primitives(primitive_parse)
        core_parse = parse_core(selected)
        graph_parse = parse_graph(core_parse)
        pairs = []

        for char in detected_char.keys():
            top_left, bottom_right = detected_char[char]
            mid_point = ((top_left[0] + bottom_right[0]) / 2, (top_left[1] + bottom_right[1]) / 2)
            for pointid, loc in core_parse.intersection_points.items():
                distance = (mid_point[0] - loc.x) ** 2 + (mid_point[1] - loc.y) ** 2
                pairs.append((distance, char, pointid))
        for pair in pairs:
            if pair[0] < 500 and pair[1] not in match_char.keys() and pair[2] not in match_char.values():
                match_char[pair[1]] = pair[2]
        for char, idx in match_char.items():
            match_char[char] = (core_parse.intersection_points[idx].x, core_parse.intersection_points[idx].y)
        # print(i, match_char)
        # cimage = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        # for char, point in match_char.items():
        #     cv2.circle(cimage, (int(point[0]), int(point[1])), 2, (0, 0, 255), 2)
        # cv2.imwrite('tmp/all_results/core{}.png'.format(i), cimage)
        extract_list.append({
            'points': get_all_instances(graph_parse, 'point').keys(),
            'lines': get_all_instances(graph_parse, 'line').keys(),
            'circles': get_all_instances(graph_parse, 'circle').keys(),
            'angles': get_all_instances(graph_parse, 'angle').keys(),
            'polygon': get_all_instances(graph_parse, 'polygon').keys(),
            'chars': detected_char,
            'match_char': match_char
        })
    except:
        print('fail"', i)
        extract_list.append(None)


with open('extracted_415.pk', 'wb') as f:
    pickle.dump(extract_list, f)
