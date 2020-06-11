from scipy import ndimage
import cv2
import numpy as np

# from geosolver.diagram.states import ImageSegment, ImageSegmentParse
from extractor.states import ImageSegment, ImageSegmentParse
# from geosolver.ontology.instantiator_definitions import instantiators
from extractor.template_matching import TemplateMatcher
from utils import *
from matplotlib import pyplot as plt

class Geometry_Extractor(object):
    def __init__(self):
        self.matcher = TemplateMatcher()

    def extract(self, image):
        kernel = np.ones((3, 3), np.uint8)
        detected_char, matched_image = self.matcher.match(image)
        labeled_image, num_objects = ndimage.label(matched_image, structure=kernel)
        # slices = ndimage.find_objects(labeled_image)
        # for idx, slice_ in enumerate(slices):
        all_pixels = (labeled_image > 0).sum()
        min_pixel = all_pixels / 20
        # small object removal
        for object_id in range(num_objects):
            boolean_array = labeled_image == (object_id + 1)
            if boolean_array.sum() <= min_pixel:
                # print(boolean_array.sum())
                matched_image = matched_image*(1-boolean_array)
        # gray = np.float32(matched_image)
        # matched_image = cv2.cvtColor(matched_image, cv2.COLOR_GRAY2BGR)
        # dst = cv2.cornerHarris(gray, 3, 3, 0.04)
        # plt.imshow(dst, cmap='gray')
        # plt.title('corner'), plt.xticks([]), plt.yticks([])
        # plt.show()
        # dst = cv2.dilate(dst, None)
        # print(dst.shape)
        # matched_image[dst > 0.01 * dst.max()] = [0, 0, 255]
        # cv2.imshow('dst', dst)
        # if cv2.waitKey(0) & 0xff == 27:
        #     cv2.destroyAllWindows()
        return matched_image


if __name__ == '__main__':
    ge = Geometry_Extractor()
    image_path = 'tmp/all_images/5432.png'
    img = cv2.imread(image_path, 0)
    image = ge.extract(img)
    # plt.imshow(image, cmap='gray')
    # plt.title('Detected Char'), plt.xticks([]), plt.yticks([])
    # plt.show()

