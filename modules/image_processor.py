import os
import cv2
from matplotlib import pyplot as plt
import albumentations as A

class ImageProcessor:
    def __init__(self, static_folder='static/processed_images'):
        self.static_folder = static_folder

    def read_and_convert(self, image_path):
        """
        Đọc ảnh từ đường dẫn và chuyển đổi từ BGR sang RGB
        """
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return image

    def save_image(self, image, filename):
        """
        Lưu ảnh đã xử lý vào static folder
        """
        if not os.path.exists(self.static_folder):
            os.makedirs(self.static_folder)

        processed_image_path = os.path.join(self.static_folder, filename)
        plt.imsave(processed_image_path, image)
        return processed_image_path

    def horizontal_flip(self, image):
        """
        Thực hiện phép biến đổi Horizontal Flip
        """
        transform = A.HorizontalFlip(p=1.0)
        augmented_image = transform(image=image)['image']
        return augmented_image

    def vertical_flip(self, image):
        """
        Thực hiện phép biến đổi Vertical Flip
        """
        transform = A.VerticalFlip(p=1.0)
        augmented_image = transform(image=image)['image']
        return augmented_image

    # Bạn có thể thêm nhiều phép biến đổi khác như sau
    def rotate_90(self, image):
        """
        Thực hiện phép biến đổi xoay 90 độ
        """
        transform = A.Rotate(limit=90, p=1.0)
        augmented_image = transform(image=image)['image']
        return augmented_image
