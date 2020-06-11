from geosolver.diagram.parse_image_segments import parse_image_segments
from geosolver.diagram.parse_primitives import parse_primitives
from geosolver.diagram.select_primitives import select_primitives
from geosolver.diagram.parse_core import parse_core
from geosolver.diagram.parse_graph import parse_graph
from geosolver.diagram.get_instances import get_all_instances
from geosolver.utils import prep
from geosolver.diagram.draw_on_image import *
from PIL import Image
# import pytesseract
# config = '--psm 6 -l equ --oem 2 configfile myconfig'
# print(pytesseract.image_to_string(Image.open('tmp/seg/A/seg14_1.png'), config=config))
# print('---')
# from extractor.parse_image_segments import parse_image_segments
import cv2
import numpy as np
from copy import deepcopy
from operator import itemgetter
from itertools import permutations
from geosolver.diagram.my_segments import Geometry_Extractor


class GeometryImageParser():
    def __init__(self):
        self.current_match = None
        self.current_graph_parse = None
        self.current_match_position = None

    def display_instances(self, inst_type="line", ids_of_insts=[]):
        all_instances = get_all_instances(self.current_graph_parse, inst_type)
        assert all_instances

        # self.current_graph_parse.display_instances(all_instances)
        # matching chars
        ids_of_insts_matched = []
        for ids_of_inst in ids_of_insts:
            ids_of_inst_matched = itemgetter(*ids_of_inst)(self.current_match)
            if ids_of_inst_matched not in all_instances.keys():
                if inst_type is "line" or inst_type is "angle":
                    ids_of_inst_matched = list(ids_of_inst_matched)
                    ids_of_inst_matched.reverse()  # line: BA -> AB, angle: ABC -> CBA
                    import ipdb; ipdb.set_trace()
                    assert tuple(ids_of_inst_matched) in all_instances.keys()
                    ids_of_insts_matched.append(tuple(ids_of_inst_matched))
                elif inst_type is "polygon":
                    for p in permutations(ids_of_inst_matched):
                       if tuple(p) in all_instances.keys():
                           ids_of_insts_matched.append(tuple(p)); break
            else:
                ids_of_insts_matched.append(ids_of_inst_matched)

        try:
            instances_filter = list(itemgetter(*ids_of_insts_matched)(all_instances))  # indices_filter: a list of tuple
        except KeyError as e:
            print(e)
        # finally:
        #     print(ids_of_insts_matched)

        self.current_graph_parse.display_instances(instances_filter, display_label=True, match_position=self.current_match_position)

    def parse_image(self, image_path="C:/Users/DM/Desktop/example_1.JPG", use_haris_centroids=True):  # image_path = 'tmp/images2/0.png'
        ge = Geometry_Extractor()
        img = cv2.imread(image_path, 0)

        ## parse image
        image_segment_parse, detected_char = ge.parse_image_segments(img)
        # cv2.imwrite('tmp/results/source1.png', image_segment_parse.diagram_image_segment.segmented_image)
        primitive_parse = parse_primitives(image_segment_parse, parse_circles=False)
        # cv2.imwrite('tmp/results/primitive1.png', primitive_parse.get_image_primitives())
        selected = select_primitives(primitive_parse)
        # cv2.imwrite('tmp/results/selected1.png', selected.get_image_primitives())
        print("Displaying primitives...")
        core_parse = parse_core(selected)  
        print("Displaying points...")
        core_parse.display_points(display_label=False)
        # cv2.imwrite('tmp/results/core1.png', core_parse.get_image_points())
        # print(core_parse.intersection_points)
        print(detected_char)
        graph_parse = parse_graph(core_parse)
        self.current_graph_parse = graph_parse

        # image = cv2.imread(image_path)
        # for line in lines.values():
        #     image = draw_line2(image, line, offset=image_segment_parse.diagram_image_segment.offset)
        # cv2.imwrite('tmp/results/im_lines.png', image)
        # image = cv2.imread(image_path)
        # for circle in circles.values():
        #     image = draw_circle2(image, circle, offset=image_segment_parse.diagram_image_segment.offset)
        # cv2.imwrite('tmp/results/im_circles.png', image)     
        
        match = {}
        candidate_pairs = []
        for char in detected_char.keys():
            top_left, bottom_right = detected_char[char]
            mid_point = ((top_left[0]+bottom_right[0])/2, (top_left[1]+bottom_right[1])/2)
            for pointid, loc in core_parse.intersection_points.items():
                distance = (mid_point[0] - loc.x)**2 + (mid_point[1] - loc.y)**2
                candidate_pairs.append((distance, char, pointid))
        candidate_pairs.sort(key=lambda x: x[0])
        for pair in candidate_pairs:
            if pair[0] < 500 and pair[1] not in match.keys() and pair[2] not in match.values():
                match[pair[1]] = pair[2]
        self.current_match = deepcopy(match)
        print(match)
        for char, idx in match.items():
            match[char] = core_parse.intersection_points[idx]
        self.current_match_position = match
        print(match)


        ## harris centroids detection, refer: https://docs.opencv.org/3.4/dc/d0d/tutorial_py_features_harris.html
        if use_haris_centroids:
            import ipdb; ipdb.set_trace()
            # find Harris corners
            origin_img = core_parse.image_segment_parse.get_colored_original_image()
            gray_img = cv2.cvtColor(origin_img, cv2.COLOR_BGR2GRAY)
            gray_img = np.float32(gray_img)
            # cv2.imwrite("corner.png", gray_img)
            # Harris_detector = cv2.cornerHarris(gray_img, 7, 3, 0.08)  
            Harris_detector = cv2.cornerHarris(gray_img, 5, 3, 0.04)   
            cv2.imwrite("corner1.png", Harris_detector)
            dst = cv2.dilate(Harris_detector, None)
            cv2.imwrite("corner2.png", dst)
            img_2 = cv2.imread(image_path)
            # img_2[dst>0.01*dst.max()] = [255, 0, 0]
            # cv2.imwrite('corner3.png', img_2)
            
            # find centroids
            ret, dst = cv2.threshold(dst,0.01*dst.max(), 255, 0)
            dst = np.uint8(dst)
            _, _, _, centroids = cv2.connectedComponentsWithStats(dst)
        
            # Now draw centroids
            for xy in centroids:
                xy_int = xy.copy().astype(int)
                cv2.circle(img_2, tuple(xy_int), 1, (255, 0, 0), thickness = -1)
                cv2.putText(img_2, str(xy_int), tuple(xy_int), cv2.FONT_HERSHEY_PLAIN,
                            1.0, (0,0,0), thickness = 1)
            cv2.imwrite("image.png", img_2)
            
            new_match = {}
            new_candidate_pairs = []
            for char, position in match.items():
                for centroid in centroids:
                    distance = (centroid[0] - position.x)**2 + (centroid[1] - position.y)**2
                    new_candidate_pairs.append((distance, char, centroid.tolist()))
            new_candidate_pairs.sort(key=lambda x: x[0])
            for pair in new_candidate_pairs:
                if pair[1] not in new_match.keys() and pair[2] not in new_match.values():
                    new_match[pair[1]] = pair[2]
            self.current_match_position = new_match
            print("new_match:", new_match)

        # HACK: restore format and rerank by letter-order
        coordinates = []
        for char, coo in self.current_match_position.items():
            if use_haris_centroids:
                coordinates.append("{0}({1}+7,{2}-24)".format(char, coo[0], coo[1]))
            else:
                coordinates.append("{0}({1}+7,{2}-24)".format(char, coo.x, coo.y))
        coordinates.sort(key=lambda x: x[0])             
        
        return " ".join(coordinates)


if __name__ == "__main__":
    gimg_parser = GeometryImageParser()
    gimg_parser.parse_image()