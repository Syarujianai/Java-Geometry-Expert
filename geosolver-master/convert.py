# process transparent images

import cv2
import os

image_path = 'tmp/all_images/{}.png'
result_path = 'tmp/all_results/'

knt = 0
for i in range(len(os.listdir('tmp/all_images/'))):   # len(os.listdir('tmp/all_images/')))
    # if i % 1 == 0:
    #     print(i)
    match_char = {}
    image = cv2.imread(image_path.format(i), -1)
    flag = 0
    if image.shape[2] == 4:
        for x in range(image.shape[0]):
            for y in range(image.shape[1]):
                color_d = image[x, y]
                if color_d[3] == 0:
                    flag = 1
                    image[x,y] = [255, 255, 255, 255]
    cv2.imwrite('tmp/images2/{}.png'.format(i), image)

    if flag:
        print i
        knt += 1

print(knt)
