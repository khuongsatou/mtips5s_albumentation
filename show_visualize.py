import cv2
from matplotlib import pyplot as plt


def visualize(image):
    plt.figure(figsize=(10, 10))
    plt.axis('off')
    plt.imshow(image)
    plt.show()

def show_visualize():
    image = cv2.imread('images/image_3.jpg')
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    visualize(image)
    print("In File: show_visualize.py, Line: 14","DONE")

if __name__ == '__main__':
    show_visualize()