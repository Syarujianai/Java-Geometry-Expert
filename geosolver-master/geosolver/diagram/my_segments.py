from scipy import ndimage
import cv2
import numpy as np

from geosolver.diagram.states import ImageSegment, ImageSegmentParse
from geosolver.ontology.instantiator_definitions import instantiators
from geosolver.utils import prep
from geosolver.diagram.template_matching import TemplateMatcher


class Geometry_Extractor(object):
    def __init__(self):
        self.matcher = TemplateMatcher()

    def parse_image_segments(self, image):
        kernel = np.ones((3, 3), np.uint8)
        detected_char, source_image, matched_image = self.matcher.match(image)
        labeled_image, num_objects = ndimage.label(matched_image, structure=kernel)
        all_pixels = (labeled_image > 0).sum()
        min_pixel = all_pixels / 20

        for object_id in range(num_objects):
            boolean_array = labeled_image == (object_id + 1)
            if boolean_array.sum() <= min_pixel:
                # print(boolean_array.sum())
                matched_image = (matched_image * (1 - boolean_array)).astype(np.uint8)
        boolean_array = matched_image > 0
        offset = instantiators['point'](0, 0)
        pixels = set(instantiators['point'](x, y) for x, y in np.transpose(np.nonzero(np.transpose(boolean_array))))
        idx = 0
        # print(matched_image.dtype)
        diagram_segment = ImageSegment(source_image, source_image, matched_image, pixels, offset, idx)
        image_segment_parse = ImageSegmentParse(image, diagram_segment, {})
        return image_segment_parse, detected_char


# def _get_image_segments(image, kernel, block_size, c):
#     binarized_image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
#                                             cv2.THRESH_BINARY_INV, block_size, c)
#     # ret, binarized_image2 = cv2.threshold(image, cv2.THRESH_OTSU, 255, cv2.THRESH_BINARY)
#     # print(ret)
#     # cv2.imshow('b1',255-binarized_image)
#     # cv2.waitKey()
#     # cv2.destroyAllWindows()
#     # cv2.imshow('b2',binarized_image2)
#     # cv2.waitKey()
#     # cv2.destroyAllWindows()
#
#     labeled, nr_objects = ndimage.label(binarized_image, structure=kernel)
#     slices = ndimage.find_objects(labeled)
#     # print(slices)
#     # remove small object and detect the left
#
#     for idx, slice_ in enumerate(slices):
#         offset = instantiators['point'](slice_[1].start, slice_[0].start)
#         sliced_image = image[slice_]
#         boolean_array = labeled[slice_] == (idx+1)
#         segmented_image = 255 - (255-sliced_image) * boolean_array
#         pixels = set(instantiators['point'](x, y) for x, y in np.transpose(np.nonzero(np.transpose(boolean_array))))
#         binarized_segmented_image = cv2.adaptiveThreshold(segmented_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
#                                                           cv2.THRESH_BINARY_INV, block_size, c)
#         # ret, binarized_segmented_image = cv2.threshold(segmented_image, cv2.THRESH_OTSU, 255, cv2.THRESH_BINARY)
#         image_segment = ImageSegment(segmented_image, sliced_image, binarized_segmented_image, pixels, offset, idx)
#         image_segments[idx] = image_segment
#
#     return image_segments
#
#
# # diagram
# def _get_diagram_and_label_segments(image_segments, min_area, min_height, min_width):
#     # the largest segment is the diagram segment
#     diagram_segment = max(image_segments.values(), key=lambda s: s.area)
#     label_segments = {}
#     for key, image_segment in image_segments.iteritems():
#         if key == diagram_segment.key:
#             continue
#         a = image_segment.area >= min_area
#         h = image_segment.shape[1] >= min_height
#         w = image_segment.shape[0] >= min_width
#         if a and h and w:
#             label_segments[key] = image_segment
#
#     return diagram_segment, label_segments
