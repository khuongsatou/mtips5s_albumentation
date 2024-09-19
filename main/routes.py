import os
import cv2
from flask import Blueprint, jsonify, render_template, url_for,request, redirect,session
from matplotlib import pyplot as plt
from modules import image_processor
from modules.image_processor import ImageProcessor
from modules.main.main import show_visualize
from werkzeug.utils import secure_filename
from modules.image_processor import ImageProcessor
import albumentations as A
import numpy as np

from modules.transform.image_transformer import ImageTransformer
from modules.transform.transform_params import TransformParams

# Tạo Blueprint
main = Blueprint('main', __name__)

# Đường dẫn tới folder static để lưu ảnh
STATIC_FOLDER = 'static/processed_images'

# Đường dẫn để lưu ảnh upload
PROCESSED_FOLDER = 'static/processed_images'
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
# Đảm bảo thư mục tồn tại
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

# Khởi tạo đối tượng xử lý hình ảnh
image_processor = ImageProcessor()

# Kiểm tra định dạng file ảnh hợp lệ
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@main.route('/', methods=['GET'])
def homepage():
    return render_template('main/index.html')

@main.route('/v2', methods=['GET'])
def homepage_v2():
    return render_template('main/v2/index.html')


# Route để upload ảnh
@main.route('/api/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Lưu ảnh vào thư mục uploads
    if file:
        filename = secure_filename(file.filename)
        image_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(image_path)
        return jsonify({"message": "File uploaded successfully", "image_path": image_path}), 200

@main.route('/api/transform', methods=['POST'])
def transform_image():
    # Lấy toàn bộ payload từ yêu cầu
    data = request.json

    # Xử lý các thông tin cơ bản
    transform_type = data.get('transform')
    image_path = data.get('image_path')
    params = data.get('params', {})

    if not image_path or not os.path.exists(image_path):
        return jsonify({"error": "Invalid image path"}), 400

    # Lấy giá trị từ params
    p = params.get('p', 1.0)
    limit = params.get('limit', 90)
    blur = params.get('blur', 0)
    sharpen = params.get('sharpen', 0)
    brightness = params.get('brightness', 1.0)
    contrast = params.get('contrast', 1.0)
    noise = params.get('noise', 0)

    # Đọc và xử lý ảnh
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Tạo danh sách các phép biến đổi
    transforms = []

    if transform_type == 'horizontal_flip':
        transforms.append(A.HorizontalFlip(p=p))
    elif transform_type == 'vertical_flip':
        transforms.append(A.VerticalFlip(p=p))
    elif transform_type == 'rotate_90':
        transforms.append(A.Rotate(limit=(limit, limit), p=p))
    
    # Thêm các bộ lọc và biến đổi bổ sung
    if blur > 0:
        # transforms.append(A.GaussianBlur(blur_limit=blur, p=1.0))
        # Đảm bảo blur_limit luôn là số lẻ hoặc 0
        blur_limit = (blur, blur) if blur % 2 == 1 else (blur - 1, blur - 1)
        transforms.append(A.GaussianBlur(blur_limit=blur_limit, p=1.0))
    if sharpen > 0:
        transforms.append(A.Sharpen(p=1.0))
    if brightness != 1.0 or contrast != 1.0:
        transforms.append(A.RandomBrightnessContrast(brightness_limit=(brightness-1, brightness-1), contrast_limit=(contrast-1, contrast-1), p=1.0))
    if noise > 0:
        transforms.append(A.GaussNoise(var_limit=(noise, noise), p=1.0))

    # Áp dụng tất cả các phép biến đổi
    if transforms:
        transform = A.Compose(transforms)
        augmented = transform(image=image)
        image = augmented['image']

    # Lưu ảnh đã xử lý vào thư mục processed_images
    processed_image_path = os.path.join(PROCESSED_FOLDER, 'processed_image.jpg')
    plt.imsave(processed_image_path, image)

    return jsonify({"message": "Image transformed successfully", "processed_image_path": processed_image_path}), 200


@main.route('/api/transform_v2', methods=['POST'])
def transform_image_v2():
    # Lấy toàn bộ payload từ yêu cầu
    data = request.json

    # Tạo đối tượng TransformParams
    transform_params = TransformParams(data)

    # Tạo đối tượng ImageTransformer
    image_transformer = ImageTransformer(transform_params)

    # Kiểm tra đường dẫn ảnh
    is_valid, error_response, status_code = image_transformer.validate_image()
    if not is_valid:
        return jsonify(error_response), status_code

    # Đọc và xử lý ảnh
    image = image_transformer.load_image()
    image = image_transformer.apply_transforms(image)

    # Lưu ảnh đã xử lý vào thư mục processed_images
    processed_image_path = os.path.join(PROCESSED_FOLDER, 'processed_image.jpg')
    image_transformer.save_image(image, processed_image_path)

    return jsonify({"message": "Image transformed successfully", "processed_image_path": processed_image_path}), 200
