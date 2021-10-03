import cv2


class Image:
    def __init__(self, path, origin, number):
        self.origin = origin
        self.path = path
        self.number = number
        self.img = cv2.imread(self.path)
        self.size = self.img.shape[:2]

    def check_if_mid(self, mid_val):
        """
        Checks if the image is the middle piece in the puzzle
        """
        if self.number == mid_val:
            return True
        return False

    def update(self, index):
        """
        Updates the position of the image according to user's hand movements
        :param index: Of the form [x, y], denoting the position coordinates of user's index finger
        """
        height, width = self.size
        self.origin = [index[0] - width // 2, index[1] - height // 2]