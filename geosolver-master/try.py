from geosolver.diagram.parse_image_segments import parse_image_segments
from geosolver.diagram.parse_primitives import parse_primitives
from geosolver.diagram.select_primitives import select_primitives
from geosolver.diagram.parse_core import parse_core
from geosolver.diagram.parse_graph import parse_graph
from geosolver.diagram.get_instances import get_all_instances

from geosolver.utils import prep
from geosolver.diagram.draw_on_image import *
import cv2
# demonstrate the image & parse image segments
image_path = 'tmp/all_images/8765.png'

image_segment_parse = parse_image_segments(prep.open_image(image_path))
# image_segment_parse.diagram_image_segment.display_segmented_image()
# prep.save_image(image_segment_parse.diagram_image_segment.segmented_image, 'tmp/t.png')
cv2.imwrite('tmp/results/source1.png', image_segment_parse.diagram_image_segment.segmented_image)
cv2.imwrite('tmp/results/sourceb.png', 255-image_segment_parse.diagram_image_segment.binarized_segmented_image)

# parse the primitive
primitive_parse = parse_primitives(image_segment_parse)
# primitive_parse.display_primitives()
cv2.imwrite('tmp/results/primitive1.png', primitive_parse.get_image_primitives())

# select the best set of primitive
selected = select_primitives(primitive_parse)
# selected.display_primitives()
cv2.imwrite('tmp/results/selected1.png', selected.get_image_primitives())

# point clustering
core_parse = parse_core(selected)
# core_parse.display_points()
cv2.imwrite('tmp/results/core1.png', core_parse.get_image_points())

# print(core_parse.intersection_points.values())
# for point in core_parse.intersection_points:
#     print(point)

# elements fine-tuning

graph_parse = parse_graph(core_parse)
lines = get_all_instances(graph_parse, 'line')
circles = get_all_instances(graph_parse, 'circle')
arcs = get_all_instances(graph_parse, 'arc')
angles = get_all_instances(graph_parse, 'angle')
print(lines)
print(circles)
# image = core_parse.get_image_points()
image = cv2.imread(image_path)
# image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
for line in lines.values():
    image = draw_line2(image, line, offset=image_segment_parse.diagram_image_segment.offset)
cv2.imwrite('tmp/results/im_lines.png', image)

# image = cv2.imread(image_path)
for circle in circles.values():
    image = draw_circle2(image, circle, offset=image_segment_parse.diagram_image_segment.offset)
cv2.imwrite('tmp/results/im_circles.png', image)


# image = cv2.imread(image_path)
# for angle in angles.values():
#     image = draw_angle2(image, angle, offset=image_segment_parse.diagram_image_segment.offset)
# cv2.imwrite('tmp/im_angles.png', image)

# print(sum(sum(primitive_parse.image_segment_parse.original_image < 180)))
# print("Displaying lines...")
# for key, line in lines.iteritems():
#     graph_parse.display_instances([line])
# print("Displaying circles...")
# for key, circle in circles.iteritems():
#     graph_parse.display_instances([circle])
# print("Displaying arcs...")
# for key, arc in arcs.iteritems():
#     graph_parse.display_instances([arc])
# print("Displaying angles...")
# for key, angle in angles.iteritems():
#     graph_parse.display_instances([angle])

# for idx, label_image_segment in image_segment_parse.label_image_segments.iteritems():
#     cv2.imwrite('tmp/results/seg{}.png'.format(idx), label_image_segment.segmented_image)
