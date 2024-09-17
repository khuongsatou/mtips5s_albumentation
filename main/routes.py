import os
import cv2
from flask import Blueprint, jsonify, render_template, url_for,request, redirect,session
from matplotlib import pyplot as plt
from modules import image_processor
from modules.image_processor import ImageProcessor
from modules.main.main import show_visualize
from werkzeug.utils import secure_filename
from modules.image_processor import ImageProcessor

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

# Route để thực hiện transform ảnh
@main.route('/api/transform', methods=['POST'])
def transform_image():
    data = request.json
    transform_type = data.get('transform')
    image_path = data.get('image_path')

    if not image_path or not os.path.exists(image_path):
        return jsonify({"error": "Invalid image path"}), 400

    # Đọc và xử lý ảnh
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Áp dụng biến đổi dựa trên loại được chọn
    if transform_type == 'horizontal_flip':
        image = cv2.flip(image, 1)
    elif transform_type == 'vertical_flip':
        image = cv2.flip(image, 0)
    elif transform_type == 'rotate_90':
        image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)

    # Lưu ảnh đã xử lý vào thư mục processed_images
    processed_image_path = os.path.join(PROCESSED_FOLDER, 'processed_image.jpg')
    plt.imsave(processed_image_path, image)

    return jsonify({"message": "Image transformed successfully", "processed_image_path": processed_image_path}), 200
