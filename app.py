from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
from tensorflow.keras.models import load_model
import cv2
import numpy as np

app = Flask(__name__)

# Load the trained model
model = load_model('model.h5')

# Set the upload folder and allowed extensions
app.config['UPLOAD_FOLDER'] = 'static/uploaded_images'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def process_image(image_path):
    img = cv2.imread(image_path)
    img = cv2.resize(img, (224, 224))
    img = img / 255.0  # Normalize image
    img = np.expand_dims(img, axis=0)
    return img

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(url_for('index'))

    file = request.files['file']

    if file.filename == '':
        return redirect(url_for('index'))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Process the uploaded image
        processed_image = process_image(file_path)

        # Make prediction using the loaded model
        prediction = model.predict(processed_image)
        disease_label = np.argmax(prediction)
        classes = ['Healthy', 'Disease1', 'Disease2', 'Disease3']  # Replace with actual class names
        result = classes[disease_label]

        return render_template('index.html', result=result, image_path=file_path)

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
