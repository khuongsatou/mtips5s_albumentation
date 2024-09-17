import random

import cv2
from matplotlib import pyplot as plt

import albumentations as A
random.seed(7)

def visualize(image):
    plt.figure(figsize=(10, 10))
    plt.axis('off')
    plt.imshow(image)