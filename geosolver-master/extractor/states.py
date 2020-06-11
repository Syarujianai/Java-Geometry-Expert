import cv2

# from geosolver.diagram.draw_on_image import draw_point, draw_instance, draw_label
from extractor.utils import display_image

__author__ = 'minjoon'


class ImageSegment(object):
    def __init__(self, segmented_image, sliced_image, binarized_segmented_image, pixels, offset, key):
        self.sliced_image = sliced_image
        self.segmented_image = segmented_image
        self.binarized_segmented_image = binarized_segmented_image
        self.pixels = pixels
        self.offset = offset
        self.shape = segmented_image.shape
        self.key = key
        self.area = segmented_image.shape[0] * segmented_image.shape[1]

    def display_segmented_image(self, block=True):
        display_image(self.segmented_image, block=block)

    def display_binarized_segmented_image(self, block=True):
        display_image(self.binarized_segmented_image, block=block)


class ImageSegmentParse(object):
    def __init__(self, original_image, diagram_image_segment, label_image_segments):
        """
        :param numpy.ndarray original_image:
        :param ImageSegment diagram_image_segment:
        :param dict label_image_segments:
        :return:
        """
        assert isinstance(diagram_image_segment, ImageSegment)
        assert isinstance(label_image_segments, dict)
        self.original_image = original_image
        self.diagram_image_segment = diagram_image_segment
        self.label_image_segments = label_image_segments

    def get_colored_original_image(self):
        return cv2.cvtColor(self.original_image, cv2.COLOR_GRAY2BGR)

    def display_diagram(self):
        self.diagram_image_segment.display_segmented_image()

    def display_labels(self):
        for image_segment in self.label_image_segments.values():
            image_segment.display_segmented_image()

