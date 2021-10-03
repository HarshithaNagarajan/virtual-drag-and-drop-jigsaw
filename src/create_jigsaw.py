import cv2
import math
import random


class crop_image:
    def __init__(self, img, parts):
        self.h = 400
        self.w = 400
        self.img = cv2.resize(img, (self.h, self.w))
        self.parts = parts

    def store_randomly(self, order):
        """
        Shuffles the cropped images and stores in a folder
        :param order: a nested list containing cropped images with their respective original positions
        :return: a list containing original positions of the shuffled images, in the order of shuffling
        """
        # Shuffling randomly:-
        random.shuffle(order)
        for sublist in order:
            random.shuffle(sublist)

        shuffled_imgs = []  # to store cropped images one after the other (in shuffled order)
        shuffled_pos = []  # to store positions of the cropped images (in shuffled order)
        for i in range(len(order)):
            for j in range(len(order)):
                shuffled_imgs.append(order[i][j][0])
                shuffled_pos.append(order[i][j][1])

        """CHANGE DIRECTORY PATH HERE AS PER NEED """
        path = r'S:\PyCharm\Projects\virtual_jigsaw\cropped'  # to store the cropped images as .jpg's
        k = 0
        j = 1
        for i in range(len(shuffled_imgs)):
            if (i + 1) % 26 == 0:
                k += 1
                j = 1
            img_name = path + "\part_" + ('z' * k) + (chr(96 + j)) + ".jpg"
            j += 1
            cv2.imwrite(img_name, shuffled_imgs[i])

        return shuffled_pos

    def crop(self):
        """
        Crops an input image into 'n' pieces
        :return:
        1) The position value of the middle piece (middle piece in the puzzle would be fixed at the start of the game)
        2) A list of original positions of the shuffled pieces, in the shuffled order (received from 'store_randomly()')
        """
        h, w = self.h, self.w
        p = []
        mid_val = self.parts // 2
        cols = int(math.sqrt(self.parts))
        order = [[j for j in range(cols)] for i in range(cols)]
        x = h // cols
        pos = 0
        for i in range(cols):
            if i == cols - 1:
                start = i * x
                end = h
            else:
                start = i * x
                end = (i + 1) * x

            for j in range(cols):
                if j == cols - 1:
                    s = j * x
                    e = w
                else:
                    s = j * x
                    e = (j + 1) * x

                img_slice = self.img[start:end, s:e]
                p.append(img_slice)
                order[i][j] = [img_slice, pos]
                pos += 1

        shuffled_pos = self.store_randomly(order)
        return mid_val, shuffled_pos
