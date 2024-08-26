from flask import Flask, request, send_from_directory
from PIL import Image
import numpy as np
import io

app = Flask(__name__)

ASCII_CHARS = "@%#*+=-:. "

def image_to_ascii(image, new_width=100):
    width, height = image.size
    aspect_ratio = height / width
    new_height = int(new_width * aspect_ratio * 0.55)  # Ajustar por la diferencia de proporción de caracteres
    image = image.resize((new_width, new_height))

    image = image.convert('L')

    pixels = np.array(image)
    ascii_str = ""
    for row in pixels:
        for pixel in row:
            ascii_str += ASCII_CHARS[pixel // 32]
        ascii_str += "\n"

    return ascii_str

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return "No se subió ningún archivo de imagen.", 400

    image_file = request.files['image']
    image = Image.open(io.BytesIO(image_file.read()))

    ascii_art = image_to_ascii(image)
    return ascii_art

if __name__ == '__main__':
    app.run(debug=True)
