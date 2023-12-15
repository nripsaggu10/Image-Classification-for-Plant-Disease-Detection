# web_application/routes.py
from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from .image_processor import process_image
from .model_loader import load_model

web_app = Blueprint('web_app', __name__)

model = load_model('model.h5')

@web_app.route('/')
def index():
    return render_template('index.html')

@web_app.route('/upload', methods=['POST'])
def upload_file():
    # ... (existing code)
