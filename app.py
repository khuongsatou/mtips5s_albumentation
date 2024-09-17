from flask import Flask
from main import main as main_blueprint
import os
from flask_session import Session



def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config.from_object(__name__)

    Session(app)

    # Đăng ký Blueprint
    app.register_blueprint(main_blueprint)

    # Cấu hình thư mục upload
    app.config['UPLOAD_FOLDER'] = 'uploads/'

    # Đảm bảo thư mục uploads tồn tại
    if not os.path.exists('uploads'):
        os.makedirs('uploads')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True,host="0.0.0.0",port=8081)
