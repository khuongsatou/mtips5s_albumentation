import cv2

from modules.main.test import visualize


def show_visualize():
    image = cv2.imread('images/image_3.jpg')
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # visualize(image)