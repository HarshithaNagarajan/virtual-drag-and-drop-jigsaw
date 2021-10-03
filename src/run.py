import cv2
from cvzone.HandTrackingModule import HandDetector
from create_jigsaw import crop_image
from images import Image
import math
import os


def draw_grid(img, size, grid_shape):
    """
    :param img: image feed
    :param size: size of one puzzle piece
    :param grid_shape: number of rows and columns (rows=cols)
    :return: image with the grid drawn
    """
    cx = 930 - 54
    cy = 337 - 50
    size = [size[0], size[1]]
    n = grid_shape
    start_x = cx - (size[0] // 2) * (n-1)
    start_y = cy - (size[1] // 2) * (n-1)
    h, w = 400, 400
    # drawing vertical lines
    for x in range(n+1):
        cv2.line(img, (start_x + size[0]*x, start_y), (start_x+size[0]*x, start_y+h), color=(50, 50, 50), thickness=2)
    # drawing horizontal lines
    for y in range(n+1):
        cv2.line(img, (start_x, start_y+size[1]*y), (start_x+w, start_y+size[1]*y), color=(50, 50, 50), thickness=2)

    return img


def check_complete(p, n, img_list):
    """
    Checks if the arrangement of image-slices/puzzle pieces are correct
    :param p: list containing current positions of images
    :param n: number of rows and cols
    :param img_list: list containing the image objects
    :return: True if game is won, false if not
    """
    p.sort(key=lambda x: x[:][1])
    k = 0
    temp = [[j for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(n):
            temp[i][j] = p[k]
            k += 1
    for i in temp:
        i.sort()
    k = 0
    for i in range(n):
        for j in range(n):
            p[k] = temp[i][j]
            k += 1
    p1 = []

    sorted_pos = [i for i in range(n*n)]
    for ori in p:
        for imgObj in img_list:
            if ori == imgObj.origin:
                p1.append(imgObj.number)
                break

    if sorted_pos == p1:
        return True
    else:
        return False


def draw_winner(img):
    cv2.rectangle(img, (100, 100), (400, 180), (70, 255, 20), cv2.FILLED)
    cv2.putText(img, "YOU WIN :)", (120, 160), cv2.FONT_HERSHEY_PLAIN, 3, (10, 10, 10), 4)
    return img


def draw_try_more(img):
    cv2.rectangle(img, (100, 120), (480, 180), (10, 70, 200), cv2.FILLED)
    cv2.putText(img, "Incorrect, try more!", (120, 160), cv2.FONT_HERSHEY_PLAIN, 2, (10, 10, 10), 4)
    return img


def start_game(name, parts, path):

    cap = cv2.VideoCapture(0)
    w, h = 1240, 721
    cap.set(3, w)
    cap.set(4, h)
    detector = HandDetector(detectionCon=0.65)

    # Reading image
    img = cv2.imread(name)
    goal_img = img.copy()
    goal_img = cv2.resize(goal_img, (225, 225))
    goal_img = cv2.copyMakeBorder(goal_img, 5, 5, 5, 5, cv2.BORDER_CONSTANT, None, value=[0, 255, 0])

    # Cropping image
    obj = crop_image(img, parts)
    middle_index, pos = obj.crop()
    n = int(math.sqrt(parts))

    # Reading cropped images
    img_list = []
    im_path_list = os.listdir(path)

    i = cv2.imread(f'{path}/{im_path_list[0]}')
    size = i.shape[:2]
    offset = size[0] // 4
    n_imgs_row = w // 2 // size[0]

    k, j = 0, 1
    # Image pieces initialization
    for x, pathImg in enumerate(im_path_list):
        if pos[x] == middle_index:
            o = [930 - 54, 337 - 50]
            img_list.append(Image(f'{path}/{pathImg}', o, pos[x]))
        else:
            o = [10 + (offset + size[0]) * k, h - j * (size[1] + offset)]
            k += 1
            if k == n_imgs_row:
                k = 0
                j += 1
            img_list.append(Image(f'{path}/{pathImg}', o, pos[x]))

    while cap.isOpened():
        _, img = cap.read()
        img = cv2.flip(img, 1)
        hands = detector.findHands(img, flipType=False, draw=False)
        if parts%2!=0:
            img = draw_grid(img, size, n)

        if hands:
            points = hands[0]['lmList']
            # find dist
            l, _, img = detector.findDistance(points[8], points[12], img)
            if l < 60:
                index = points[8]

                for imgObj in img_list:
                    ox, oy = imgObj.origin
                    height, width = imgObj.size
                    if ox < index[0] < ox + width and oy < index[1] < oy + height:
                        if imgObj.check_if_mid(middle_index):
                            pass  # middle image is always fixed
                        else:
                            imgObj.update(index)
                            break
        p = []
        try:
            for imgObj in img_list:
                h1, w1 = imgObj.size
                ox, oy = imgObj.origin
                p.append([ox, oy])
                img[oy: oy + h1, ox:ox + w1] = imgObj.img
        except:
            pass

        if cv2.waitKey(1) & 0xFF == ord('d'):
            win = check_complete(p, n, img_list)
            if win:
                img = draw_winner(img)
                cv2.imshow('SOLVE!', img)
                cv2.waitKey(0)
            else:
                img = draw_try_more(img)
                cv2.imshow('SOLVE!', img)
                cv2.waitKey(0)

        cv2.imshow('SOLVE!', img)
        cv2.imshow('GOAL', goal_img)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


