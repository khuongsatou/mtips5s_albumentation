from flask import Blueprint, render_template
from modules.main import test

# Tạo Blueprint
main = Blueprint('main', __name__)

# Route chính của module
@main.route('/')
def home():
    return render_template('main/index.html')


