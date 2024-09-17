from flask import Flask
from main import main as main_blueprint

def create_app():
    app = Flask(__name__)

    # Đăng ký Blueprint
    app.register_blueprint(main_blueprint)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True,host="0.0.0.0",port=8081)
