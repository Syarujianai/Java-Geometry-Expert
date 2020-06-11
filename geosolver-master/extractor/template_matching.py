import cv2
import os
from extractor.utils import *
from matplotlib import pyplot as plt


class TemplateMatcher(object):
    def __init__(self):
        self.confidence = 0.8
        self.method = eval('cv2.TM_CCORR_NORMED')
        self.char_list = ['A', 'B', 'C', 'D', 'O', 'E', 'F', 'G', 'P', 'M', 'N', 'H']  # ,'F','G']
        self.templates = {}
        for char in self.char_list:
            self.templates[char] = []
            char_image_files = 'tmp/seg/{}/'.format(char)
            for file in os.listdir(char_image_files):
                image = cv2.imread(char_image_files + file, 0)
                image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                              cv2.THRESH_BINARY_INV, 13, 20)
                self.templates[char].append(image)

    def match(self, img):
        bin_img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                        cv2.THRESH_BINARY_INV, 13, 20)
        match_result = []
        for char in self.char_list:
            # match_result[char] = []
            for template in self.templates[char]:
                w, h = template.shape[::-1]
                res = cv2.matchTemplate(bin_img, template, self.method)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
                top_left = max_loc
                bottom_right = (top_left[0] + w, top_left[1] + h)
                match_result.append((max_val, char, top_left, bottom_right))
        match_result.sort(key=lambda x: x[0], reverse=True)

        detected_char = {}
        for res in match_result:
            val, char, top_left, bottom_right = res
            if char not in detected_char.keys() and val > self.confidence and not self.find_intersection(
                    detected_char.values(), top_left, bottom_right):
                # print(char, val)
                detected_char[char] = (top_left, bottom_right)
                cv2.rectangle(bin_img, top_left, bottom_right, 0, -1)
        return detected_char, bin_img

    @staticmethod
    def find_intersection(box_list, top_left, bottom_right):
        for box in box_list:
            x1, y1 = box[0]
            x2, y2 = box[1]
            x3, y3 = top_left
            x4, y4 = bottom_right
            # print(x1,y1,x2,y2,x3,y3,x4,y4)
            if x3 > x2 or x4 < x1 or y3 > y2 or y4 < y1:  # no intersection
                continue
            return True
        return False


if __name__ == "__main__":
    tm = TemplateMatcher()
    image_path = 'tmp/all_images/4019.png'
    img = cv2.imread(image_path, 0)
    char, bin_img = tm.match(img)
    plt.imshow(bin_img, cmap='gray')
    plt.title('Detected Char'), plt.xticks([]), plt.yticks([])
    plt.show()
